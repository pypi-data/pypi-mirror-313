import sys
import cv2
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QSlider,
    QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QIcon
from PyQt5.QtCore import Qt


class ClickableLabel(QLabel):
    """Custom QLabel to handle mouse press events."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.click_callback = None

    def mousePressEvent(self, event):
        if self.click_callback:
            self.click_callback(event)


class AnnotationTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # Video variables
        self.video_path = None
        self.cap = None
        self.current_frame = 0
        self.total_frames = 0

        # Separate lists for action and posture annotations
        self.action_annotations = []  # List of action annotations
        self.posture_annotations = []  # List of posture annotations

        # Current ongoing annotations per pigeon
        self.current_actions = {pigeon: None for pigeon in ['P1', 'P2', 'P3', 'P4']}
        self.current_postures = {pigeon: None for pigeon in ['P1', 'P2', 'P3', 'P4']}

        # Undo stack
        self.undo_stack = []  # Stack to track annotations for undo

        # Pigeons for which we will create timeline bars
        self.pigeons = ['P1', 'P2', 'P3', 'P4']
        self.timeline_bars = {}

        # GUI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pigeon Behavior Annotation Tool')
        self.setFixedSize(1400, 1080)  # Increased size for better visibility
        self.setWindowIcon(QIcon('icon.ico'))

        # Video display label
        self.video_label = QLabel(self)
        self.video_label.setScaledContents(True)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setStyleSheet("border: 1px solid black;")  # Added border for clarity

        # Frame information label
        self.frame_info_label = QLabel("Frame: 0 / 0", self)

        # Pigeon selection
        self.pigeon_selector = QComboBox(self)
        self.pigeon_selector.addItems(self.pigeons)

        # Behavior selection
        self.behavior_selector = QComboBox(self)
        self.behavior_selector.addItems([
            'Feeding', 'Drinking', 'Grit', 'Grooming', 'Incubation',
            'Feeding_young', 'Walking', 'Spread_wings', 'Kiss',
            'Mating', 'Fighting', 'Inflating_the_crop'
        ])
        self.behavior_selector.currentIndexChanged.connect(self.update_behavior_color)

        # Behavior color display
        self.behavior_color_display = QLabel(self)
        self.behavior_color_display.setFixedSize(50, 20)
        self.behavior_color_display.setStyleSheet("background-color: white; border: 1px solid black;")
        self.update_behavior_color()  # Initialize behavior color display

        # Posture selection
        self.posture_selector = QComboBox(self)
        self.posture_selector.addItems(['Standing', 'Lying_down', 'Tail_up', 'Motion'])
        self.posture_selector.currentIndexChanged.connect(self.update_posture_color)

        # Posture color display
        self.posture_color_display = QLabel(self)
        self.posture_color_display.setFixedSize(50, 20)
        self.posture_color_display.setStyleSheet("background-color: #e3e3e3; border: 1px solid black;")
        self.update_posture_color()  # Initialize posture color display

        # Control buttons
        self.load_button = QPushButton('Load Video', self)
        self.load_button.clicked.connect(self.load_video)

        self.import_annotation_button = QPushButton('Import Annotations', self)
        self.import_annotation_button.clicked.connect(self.import_annotations)

        self.prev_button = QPushButton('Previous Frame', self)
        self.prev_button.clicked.connect(self.prev_frame)

        self.next_button = QPushButton('Next Frame', self)
        self.next_button.clicked.connect(self.next_frame)

        self.start_action_button = QPushButton('Start Action', self)
        self.start_action_button.clicked.connect(self.start_action)

        self.end_action_button = QPushButton('End Action', self)
        self.end_action_button.clicked.connect(self.end_action)

        self.start_posture_button = QPushButton('Start Posture', self)
        self.start_posture_button.clicked.connect(self.start_posture)

        self.end_posture_button = QPushButton('End Posture', self)
        self.end_posture_button.clicked.connect(self.end_posture)

        self.export_button = QPushButton('Export Annotations', self)
        self.export_button.clicked.connect(self.export_annotations)

        self.export_sorted_button = QPushButton('Export Sorted Format', self)
        self.export_sorted_button.clicked.connect(self.export_sorted_annotations)

        # Undo button
        self.undo_button = QPushButton('Undo', self)
        self.undo_button.clicked.connect(self.undo_last_annotation)

        # Video progress bar
        self.progress_slider = QSlider(Qt.Horizontal, self)
        self.progress_slider.sliderMoved.connect(self.slider_moved)

        # Timeline layout for each pigeon
        timeline_layout = QVBoxLayout()
        for pigeon in self.pigeons:
            # Behavior timeline
            row_layout_behavior = QHBoxLayout()
            label_behavior = QLabel(f"{pigeon}_B", self)
            timeline_bar_behavior = ClickableLabel(self)
            timeline_bar_behavior.setFixedHeight(20)
            timeline_bar_behavior.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            timeline_bar_behavior.setStyleSheet("background-color: white; border: 1px solid black;")
            # Use default arguments to capture current pigeon and bar_type
            timeline_bar_behavior.click_callback = lambda event, pid=pigeon, bar="B": self.timeline_clicked(event, pid, bar)
            self.timeline_bars[f"{pigeon}_B"] = timeline_bar_behavior

            row_layout_behavior.addWidget(label_behavior)
            row_layout_behavior.addWidget(timeline_bar_behavior)
            timeline_layout.addLayout(row_layout_behavior)

            # Posture timeline
            row_layout_posture = QHBoxLayout()
            label_posture = QLabel(f"{pigeon}_S", self)
            timeline_bar_posture = ClickableLabel(self)
            timeline_bar_posture.setFixedHeight(20)
            timeline_bar_posture.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            timeline_bar_posture.setStyleSheet("background-color: #e3e3e3; border: 1px solid black;")
            # Use default arguments to capture current pigeon and bar_type
            timeline_bar_posture.click_callback = lambda event, pid=pigeon, bar="S": self.timeline_clicked(event, pid, bar)
            self.timeline_bars[f"{pigeon}_S"] = timeline_bar_posture

            row_layout_posture.addWidget(label_posture)
            row_layout_posture.addWidget(timeline_bar_posture)
            timeline_layout.addLayout(row_layout_posture)

            # Add a line separator between each pigeon section
            line_separator = QLabel(self)
            line_separator.setFixedHeight(1)
            line_separator.setStyleSheet("background-color: black;")
            timeline_layout.addWidget(line_separator)

        # Layout for controls
        controls_layout1 = QHBoxLayout()
        controls_layout1.addWidget(self.load_button)
        controls_layout1.addWidget(self.import_annotation_button)
        controls_layout1.addWidget(QLabel("Select Pigeon:", self))
        controls_layout1.addWidget(self.pigeon_selector)
        controls_layout1.addWidget(self.prev_button)
        controls_layout1.addWidget(self.next_button)
        controls_layout1.addWidget(self.export_button)
        controls_layout1.addWidget(self.export_sorted_button)
        controls_layout1.addWidget(self.undo_button)  # 添加Undo按钮

        controls_layout2 = QHBoxLayout()
        controls_layout2.addWidget(QLabel("Behavior:", self))
        controls_layout2.addWidget(self.behavior_selector)
        controls_layout2.addWidget(self.behavior_color_display)
        controls_layout2.addWidget(self.start_action_button)
        controls_layout2.addWidget(self.end_action_button)
        controls_layout2.addWidget(QLabel("Posture:", self))
        controls_layout2.addWidget(self.posture_selector)
        controls_layout2.addWidget(self.posture_color_display)
        controls_layout2.addWidget(self.start_posture_button)
        controls_layout2.addWidget(self.end_posture_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_label)
        main_layout.addWidget(self.frame_info_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.progress_slider)
        main_layout.addLayout(timeline_layout)
        main_layout.addLayout(controls_layout1)
        main_layout.addLayout(controls_layout2)

        # Set main layout
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def get_behavior_color(self, action_label):
        behavior_color_map = {
            'Feeding': QColor("red"),
            'Drinking': QColor("blue"),
            'Grit': QColor("green"),
            'Grooming': QColor("cyan"),
            'Incubation': QColor("magenta"),
            'Feeding_young': QColor("yellow"),
            'Walking': QColor("orange"),
            'Spread_wings': QColor("violet"),
            'Kiss': QColor("darkred"),
            'Mating': QColor("darkblue"),
            'Fighting': QColor("darkgreen"),
            'Inflating_the_crop': QColor("darkcyan")
        }
        return behavior_color_map.get(action_label, Qt.white)  # 默认白色

    def get_posture_color(self, posture_label):
        posture_color_map = {
            'Standing': QColor("purple"),
            'Lying_down': QColor("brown"),
            'Tail_up': QColor("pink"),
            'Motion': QColor("orange")
        }
        return posture_color_map.get(posture_label, QColor(211, 211, 211))  # 默认浅灰色

    def update_behavior_color(self):
        behavior = self.behavior_selector.currentText()
        color = "white"
        if behavior == 'Feeding':
            color = "red"
        elif behavior == 'Drinking':
            color = "blue"
        elif behavior == 'Grit':
            color = "green"
        elif behavior == 'Grooming':
            color = "cyan"
        elif behavior == 'Incubation':
            color = "magenta"
        elif behavior == 'Feeding_young':
            color = "yellow"
        elif behavior == 'Walking':
            color = "orange"
        elif behavior == 'Spread_wings':
            color = "violet"
        elif behavior == 'Kiss':
            color = "darkred"
        elif behavior == 'Mating':
            color = "darkblue"
        elif behavior == 'Fighting':
            color = "darkgreen"
        elif behavior == 'Inflating_the_crop':
            color = "darkcyan"
        self.behavior_color_display.setStyleSheet(f"background-color: {color}; border: 1px solid black;")

    def update_posture_color(self):
        posture = self.posture_selector.currentText()
        color = "#e3e3e3"
        if posture == 'Standing':
            color = "purple"
        elif posture == 'Lying_down':
            color = "brown"
        elif posture == 'Tail_up':
            color = "pink"
        elif posture == 'Motion':
            color = "orange"
        self.posture_color_display.setStyleSheet(f"background-color: {color}; border: 1px solid black;")

    def load_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, 'Open Video')
        if self.video_path:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                QMessageBox.critical(self, "Error", "Cannot open video.")
                return

            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.progress_slider.setRange(0, self.total_frames - 1)
            self.current_frame = 0
            self.action_annotations.clear()
            self.posture_annotations.clear()
            self.undo_stack.clear()
            self.current_actions = {pigeon: None for pigeon in self.pigeons}
            self.current_postures = {pigeon: None for pigeon in self.pigeons}
            self.update_frame_info()
            self.show_frame()
            self.update_timeline()  # 初始化时间线

    def show_frame(self):
        if not self.cap or not self.cap.isOpened():
            return
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.cap.read()
        if not ret:
            QMessageBox.critical(self, "Error", f"Cannot read frame {self.current_frame}.")
            return
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]
        qimg = QImage(frame.data, w, h, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))
        self.progress_slider.setValue(self.current_frame)
        self.update_frame_info()
        # 不在每次显示帧时更新时间线，而在需要时更新时间线

    def update_frame_info(self):
        self.frame_info_label.setText(f"Frame: {self.current_frame} / {self.total_frames}")

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.show_frame()

    def next_frame(self):
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1
            self.show_frame()

    def slider_moved(self, position):
        self.current_frame = position
        self.show_frame()
        self.update_timeline()

    def start_action(self):
        pigeon = self.pigeon_selector.currentText()
        behavior = self.behavior_selector.currentText()

        if self.current_actions[pigeon]:
            QMessageBox.warning(self, "Warning", f"Finish the current action annotation for {pigeon} before starting a new one.")
            return

        self.current_actions[pigeon] = {
            'pigeon_id': pigeon,
            'action_label': behavior,
            'start_frame': self.current_frame,
            'end_frame': None
        }

        print(f"Started action for {pigeon}: {self.current_actions[pigeon]}")  # Debugging

        self.update_timeline()

    def end_action(self):
        pigeon = self.pigeon_selector.currentText()

        if not self.current_actions[pigeon]:
            QMessageBox.warning(self, "Warning", f"No action is currently being annotated for {pigeon}.")
            return

        self.current_actions[pigeon]['end_frame'] = self.current_frame
        annotation = self.current_actions[pigeon].copy()
        annotation['posture_label'] = -1  # Posture default -1

        self.action_annotations.append(annotation)
        self.undo_stack.append(('action', annotation))

        print(f"Ended action for {pigeon}: {annotation}")  # Debugging

        self.current_actions[pigeon] = None
        self.update_timeline()

    def start_posture(self):
        pigeon = self.pigeon_selector.currentText()
        posture = self.posture_selector.currentText()

        if self.current_postures[pigeon]:
            QMessageBox.warning(self, "Warning", f"Finish the current posture annotation for {pigeon} before starting a new one.")
            return

        self.current_postures[pigeon] = {
            'pigeon_id': pigeon,
            'posture_label': posture,
            'start_frame': self.current_frame,
            'end_frame': None
        }

        print(f"Started posture for {pigeon}: {self.current_postures[pigeon]}")  # Debugging

        self.update_timeline()

    def end_posture(self):
        pigeon = self.pigeon_selector.currentText()

        if not self.current_postures[pigeon]:
            QMessageBox.warning(self, "Warning", f"No posture is currently being annotated for {pigeon}.")
            return

        self.current_postures[pigeon]['end_frame'] = self.current_frame
        annotation = self.current_postures[pigeon].copy()
        annotation['action_label'] = -1  # Action default -1

        self.posture_annotations.append(annotation)
        self.undo_stack.append(('posture', annotation))

        print(f"Ended posture for {pigeon}: {annotation}")  # Debugging

        self.current_postures[pigeon] = None
        self.update_timeline()

    def import_annotations(self):
        if not self.cap or not self.cap.isOpened():
            QMessageBox.warning(self, "Error", "Please load a video before importing annotations.")
            return

        annotation_path, _ = QFileDialog.getOpenFileName(
            self, 'Open Annotation File', '', 'CSV Files (*.csv)'
        )
        if not annotation_path:
            return

        try:
            imported_annotations = pd.read_csv(annotation_path)

            # 打印CSV文件的列名以进行调试
            print("Imported CSV Columns:", imported_annotations.columns.tolist())

            # 检查CSV是否包含必要的列
            required_columns = {'frame_id', 'pigeon_id', 'action_label', 'posture_label'}
            if not required_columns.issubset(imported_annotations.columns):
                QMessageBox.critical(
                    self, "Error", f"CSV文件缺少必要的列: {required_columns}\n实际列名: {imported_annotations.columns.tolist()}"
                )
                return

            # 检查标注帧是否超过视频帧数
            max_frame_id = imported_annotations['frame_id'].max()
            if max_frame_id >= self.total_frames:
                QMessageBox.critical(
                    self, "Error", "Annotation frame count exceeds the video frame count."
                )
                return

            # 清空现有的注释和撤销堆栈
            self.action_annotations.clear()
            self.posture_annotations.clear()
            self.undo_stack.clear()
            self.current_actions = {pigeon: None for pigeon in self.pigeons}
            self.current_postures = {pigeon: None for pigeon in self.pigeons}

            # 处理导入的注释，合并连续的相同标注
            for pigeon in self.pigeons:
                # 处理行为注释
                pigeon_actions = imported_annotations[
                    (imported_annotations['pigeon_id'] == pigeon) &
                    (imported_annotations['action_label'] != -1)
                ].sort_values('frame_id')
                if not pigeon_actions.empty:
                    grouped_actions = self.merge_consecutive_annotations(
                        pigeon_actions, 'action_label'
                    )
                    for group in grouped_actions:
                        annotation = {
                            'pigeon_id': pigeon,
                            'action_label': group['action_label'],  # 使用正确的键名
                            'start_frame': group['start_frame'],
                            'end_frame': group['end_frame'],
                            'posture_label': -1
                        }
                        self.action_annotations.append(annotation)
                        self.undo_stack.append(('action', annotation))
                        print(f"Imported action: {annotation}")  # Debugging

                # 处理姿势注释
                pigeon_postures = imported_annotations[
                    (imported_annotations['pigeon_id'] == pigeon) &
                    (imported_annotations['posture_label'] != -1)
                ].sort_values('frame_id')
                if not pigeon_postures.empty:
                    grouped_postures = self.merge_consecutive_annotations(
                        pigeon_postures, 'posture_label'
                    )
                    for group in grouped_postures:
                        annotation = {
                            'pigeon_id': pigeon,
                            'posture_label': group['posture_label'],  # 使用正确的键名
                            'start_frame': group['start_frame'],
                            'end_frame': group['end_frame'],
                            'action_label': -1
                        }
                        self.posture_annotations.append(annotation)
                        self.undo_stack.append(('posture', annotation))
                        print(f"Imported posture: {annotation}")  # Debugging

            QMessageBox.information(self, "Success", "Annotations imported successfully.")
            self.update_timeline()  # Update timeline display

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load annotations: {str(e)}')

    def merge_consecutive_annotations(self, df, label_column):
        """
        合并连续的相同标签注释。
        """
        grouped = []
        current_label = None
        start_frame = None
        end_frame = None

        for _, row in df.iterrows():
            label = row[label_column]
            frame = row['frame_id']
            if label != current_label:
                if current_label is not None:
                    grouped.append({
                        label_column: current_label,  # 使用传入的 label_column
                        'start_frame': start_frame,
                        'end_frame': end_frame
                    })
                current_label = label
                start_frame = frame
                end_frame = frame
            else:
                end_frame = frame

        # 添加最后一组
        if current_label is not None:
            grouped.append({
                label_column: current_label,  # 使用传入的 label_column
                'start_frame': start_frame,
                'end_frame': end_frame
            })

        return grouped

    def update_timeline(self):
        for pigeon in self.pigeons:
            timeline_bar_behavior = self.timeline_bars[f"{pigeon}_B"]
            timeline_bar_posture = self.timeline_bars[f"{pigeon}_S"]

            # 获取时间线尺寸
            behavior_width = timeline_bar_behavior.width()
            behavior_height = timeline_bar_behavior.height()
            posture_width = timeline_bar_posture.width()
            posture_height = timeline_bar_posture.height()

            # 创建QImage并填充默认颜色
            timeline_image_behavior = QImage(behavior_width, behavior_height, QImage.Format_RGB32)
            timeline_image_behavior.fill(Qt.white)  # 默认白色

            timeline_image_posture = QImage(posture_width, posture_height, QImage.Format_RGB32)
            timeline_image_posture.fill(QColor(211, 211, 211))  # 默认浅灰色

            # 创建颜色数组
            behavior_colors = [Qt.white] * self.total_frames
            posture_colors = [QColor(211, 211, 211)] * self.total_frames

            # 应用行为注释
            for annotation in self.action_annotations:
                if annotation['pigeon_id'] != pigeon:
                    continue
                start = annotation['start_frame']
                end = annotation['end_frame']
                color = self.get_behavior_color(annotation['action_label'])
                for frame in range(start, end + 1):
                    if 0 <= frame < self.total_frames:
                        behavior_colors[frame] = color

            # 应用姿势注释
            for annotation in self.posture_annotations:
                if annotation['pigeon_id'] != pigeon:
                    continue
                start = annotation['start_frame']
                end = annotation['end_frame']
                color = self.get_posture_color(annotation['posture_label'])
                for frame in range(start, end + 1):
                    if 0 <= frame < self.total_frames:
                        posture_colors[frame] = color

            # 应用当前进行中的行为注释（如果有）
            current_action = self.current_actions[pigeon]
            if current_action:
                start = current_action['start_frame']
                if 0 <= start < self.total_frames:
                    behavior_colors[start] = QColor("black")  # 黑线
                # 填充后续帧
                action_color = self.get_behavior_color(current_action['action_label'])
                for frame in range(start + 1, self.current_frame + 1):
                    if 0 <= frame < self.total_frames:
                        behavior_colors[frame] = action_color

            # 应用当前进行中的姿势注释（如果有）
            current_posture = self.current_postures[pigeon]
            if current_posture:
                start = current_posture['start_frame']
                if 0 <= start < self.total_frames:
                    posture_colors[start] = QColor("black")  # 黑线
                # 填充后续帧
                posture_color = self.get_posture_color(current_posture['posture_label'])
                for frame in range(start + 1, self.current_frame + 1):
                    if 0 <= frame < self.total_frames:
                        posture_colors[frame] = posture_color

            # 绘制行为时间线
            painter_behavior = QPainter(timeline_image_behavior)
            for frame in range(self.total_frames):
                x = int(frame / self.total_frames * behavior_width)
                if x >= behavior_width:
                    x = behavior_width - 1
                painter_behavior.setPen(Qt.NoPen)
                painter_behavior.setBrush(behavior_colors[frame])
                painter_behavior.drawRect(x, 0, 1, behavior_height)
            painter_behavior.end()

            # 绘制姿势时间线
            painter_posture = QPainter(timeline_image_posture)
            for frame in range(self.total_frames):
                x = int(frame / self.total_frames * posture_width)
                if x >= posture_width:
                    x = posture_width - 1
                painter_posture.setPen(Qt.NoPen)
                painter_posture.setBrush(posture_colors[frame])
                painter_posture.drawRect(x, 0, 1, posture_height)
            painter_posture.end()

            # 更新QLabel显示
            timeline_bar_behavior.setPixmap(QPixmap.fromImage(timeline_image_behavior))
            timeline_bar_posture.setPixmap(QPixmap.fromImage(timeline_image_posture))

    def undo_last_annotation(self):
        if self.undo_stack:
            annotation_type, last_annotation = self.undo_stack.pop()
            pigeon_id = last_annotation['pigeon_id']
            if annotation_type == 'action':
                if last_annotation in self.action_annotations:
                    self.action_annotations.remove(last_annotation)
                    print(f"Undo action for {pigeon_id}: {last_annotation}")  # Debugging
            elif annotation_type == 'posture':
                if last_annotation in self.posture_annotations:
                    self.posture_annotations.remove(last_annotation)
                    print(f"Undo posture for {pigeon_id}: {last_annotation}")  # Debugging
            QMessageBox.information(self, "Undo", "Last annotation removed.")
            self.update_timeline()
        else:
            QMessageBox.warning(self, "Undo", "No annotation to undo.")

    def export_annotations(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Annotations', '', 'CSV Files (*.csv)'
        )
        if save_path:
            try:
                # Combine action and posture annotations
                combined_annotations = []
                for annotation in self.action_annotations:
                    combined_annotations.append({
                        'frame_id': annotation['start_frame'],
                        'pigeon_id': annotation['pigeon_id'],
                        'action_label': annotation['action_label'],
                        'posture_label': -1
                    })
                for annotation in self.posture_annotations:
                    combined_annotations.append({
                        'frame_id': annotation['start_frame'],
                        'pigeon_id': annotation['pigeon_id'],
                        'action_label': -1,
                        'posture_label': annotation['posture_label']
                    })
                df = pd.DataFrame(combined_annotations, columns=['frame_id', 'pigeon_id', 'action_label', 'posture_label'])
                df.to_csv(save_path, index=False)
                QMessageBox.information(self, 'Success', 'Annotations saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save annotations: {str(e)}')

    def export_sorted_annotations(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Sorted Annotations', '', 'CSV Files (*.csv)'
        )
        if save_path:
            try:
                sorted_annotations = []
                for frame_id in range(self.total_frames):
                    for pigeon in self.pigeons:
                        action_label = -1
                        posture_label = -1
                        for annotation in self.action_annotations:
                            if annotation['pigeon_id'] == pigeon and annotation['start_frame'] <= frame_id <= annotation['end_frame']:
                                action_label = annotation['action_label']
                                break  # Assume one action per frame per pigeon
                        for annotation in self.posture_annotations:
                            if annotation['pigeon_id'] == pigeon and annotation['start_frame'] <= frame_id <= annotation['end_frame']:
                                posture_label = annotation['posture_label']
                                break  # Assume one posture per frame per pigeon
                        sorted_annotations.append({
                            'frame_id': frame_id,
                            'pigeon_id': pigeon,
                            'action_label': action_label,
                            'posture_label': posture_label
                        })
                df_sorted = pd.DataFrame(sorted_annotations, columns=['frame_id', 'pigeon_id', 'action_label', 'posture_label'])
                df_sorted.to_csv(save_path, index=False)
                QMessageBox.information(self, 'Success', 'Sorted annotations saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save sorted annotations: {str(e)}')

    def timeline_clicked(self, event, pigeon_id, bar_type):
        """Handle clicks on the timeline bars."""
        timeline_label = self.timeline_bars[f"{pigeon_id}_{bar_type}"]
        click_x = event.pos().x()
        total_width = timeline_label.width()
        frame_clicked = int(click_x / total_width * self.total_frames)

        found_annotation = False

        if bar_type == "B":
            # Check action annotations
            for annotation in self.action_annotations:
                if annotation['pigeon_id'] == pigeon_id:
                    if annotation['start_frame'] <= frame_clicked <= annotation['end_frame']:
                        QMessageBox.information(
                            self, "Annotation Info",
                            f"Pigeon: {pigeon_id}\n"
                            f"Type: Behavior\n"
                            f"Label: {annotation['action_label']}\n"
                            f"Start Frame: {annotation['start_frame']}\n"
                            f"End Frame: {annotation['end_frame']}"
                        )
                        found_annotation = True
                        break
            # Check current ongoing action
            current_action = self.current_actions[pigeon_id]
            if not found_annotation and current_action:
                if current_action['start_frame'] <= frame_clicked <= self.current_frame:
                    QMessageBox.information(
                        self, "Annotation Info",
                        f"Pigeon: {pigeon_id}\n"
                        f"Type: Behavior (Ongoing)\n"
                        f"Label: {current_action['action_label']}\n"
                        f"Start Frame: {current_action['start_frame']}\n"
                        f"End Frame: {self.current_frame}"
                    )
                    found_annotation = True

        elif bar_type == "S":
            # Check posture annotations
            for annotation in self.posture_annotations:
                if annotation['pigeon_id'] == pigeon_id:
                    if annotation['start_frame'] <= frame_clicked <= annotation['end_frame']:
                        QMessageBox.information(
                            self, "Annotation Info",
                            f"Pigeon: {pigeon_id}\n"
                            f"Type: Posture\n"
                            f"Label: {annotation['posture_label']}\n"
                            f"Start Frame: {annotation['start_frame']}\n"
                            f"End Frame: {annotation['end_frame']}"
                        )
                        found_annotation = True
                        break
            # Check current ongoing posture
            current_posture = self.current_postures[pigeon_id]
            if not found_annotation and current_posture:
                if current_posture['start_frame'] <= frame_clicked <= self.current_frame:
                    QMessageBox.information(
                        self, "Annotation Info",
                        f"Pigeon: {pigeon_id}\n"
                        f"Type: Posture (Ongoing)\n"
                        f"Label: {current_posture['posture_label']}\n"
                        f"Start Frame: {current_posture['start_frame']}\n"
                        f"End Frame: {self.current_frame}"
                    )
                    found_annotation = True

        if not found_annotation:
            QMessageBox.information(self, "Annotation Info", "No annotation found for this position.")

    def keyPressEvent(self, event):
        """Handle key press events for shortcuts."""
        key = event.key()

        # Navigation shortcuts
        if key == Qt.Key_D:  # Pressing 'D' for Next Frame
            self.next_frame()
        elif key == Qt.Key_S:  # Pressing 'S' for Previous Frame
            self.prev_frame()

        # Undo shortcut (Ctrl+Z)
        elif key == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.undo_last_annotation()

        # Pigeon selection shortcuts
        elif key == Qt.Key_1:  # Pressing '1' for P1
            self.pigeon_selector.setCurrentIndex(0)
        elif key == Qt.Key_2:  # Pressing '2' for P2
            self.pigeon_selector.setCurrentIndex(1)
        elif key == Qt.Key_3:  # Pressing '3' for P3
            self.pigeon_selector.setCurrentIndex(2)
        elif key == Qt.Key_4:  # Pressing '4' for P4
            self.pigeon_selector.setCurrentIndex(3)


def main():
    app = QApplication(sys.argv)
    ex = AnnotationTool()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
