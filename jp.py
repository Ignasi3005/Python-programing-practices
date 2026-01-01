import sys
import random
import webbrowser
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton, QDialog,
    QMessageBox, QFrame, QTableWidget, QTableWidgetItem, QProgressBar,
    QComboBox, QDateEdit, QTabWidget, QScrollArea, QSpinBox, QTextEdit,
    QFileDialog, QCalendarWidget, QCheckBox, QSlider, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer, QDateTime, QSize, QPropertyAnimation, QRect, QUrl
from PySide6.QtGui import QFont, QColor, QIcon, QPixmap, QPainter, QBrush, QPen
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries, QPieSlice, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtCore import QPointF
from PySide6.QtWebEngineWidgets import QWebEngineView
# QWebEnginePage lives in QtWebEngineCore on some PySide6 builds
try:
    from PySide6.QtWebEngineCore import QWebEnginePage
except Exception:
    QWebEnginePage = None
import requests
from datetime import date

# For translator
try:
    from googletrans import Translator
except:
    Translator = None


class ModernLineEdit(QLineEdit):
    """Modern styled line edit with placeholder"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(45)


class ModernPushButton(QPushButton):
    """Modern styled push button"""
    def __init__(self, text="", is_primary=True):
        super().__init__(text)
        self.setMinimumHeight(45)
        self.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)


class MetricCard(QFrame):
    """High-end metric card for displaying KPIs"""
    
    def __init__(self, title, value, unit="", icon_char="📊"):
        super().__init__()
        self.title_text = title
        self.value_text = str(value)
        self.unit_text = unit
        self.icon_char = icon_char
        self.init_ui()
        self.apply_styling()
        
    def init_ui(self):
        """Initialize metric card UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Icon and Title
        header_layout = QHBoxLayout()
        icon_label = QLabel(self.icon_char)
        icon_label.setFont(QFont("Arial", 24))
        header_layout.addWidget(icon_label)
        
        title = QLabel(self.title_text)
        title.setFont(QFont("Segoe UI", 11))
        title.setStyleSheet("color: #7f8c8d; font-weight: 500;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(self.value_text)
        value_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        value_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(value_label)
        
        # Unit
        if self.unit_text:
            unit_label = QLabel(self.unit_text)
            unit_label.setFont(QFont("Segoe UI", 12))
            unit_label.setStyleSheet("color: #3498db; font-weight: 500;")
            layout.addWidget(unit_label)
        
        layout.addStretch()
        
    def apply_styling(self):
        """Apply modern card styling"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            MetricCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #ecf0f1;
            }
        """)
        # Add a native drop shadow effect (Qt stylesheet doesn't support CSS box-shadow)
        try:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(12)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 30))
            self.setGraphicsEffect(shadow)
        except Exception:
            pass
        
    def update_value(self, new_value):
        """Update metric value"""
        self.value_text = str(new_value)
        # Refresh UI
        for widget in self.findChildren(QLabel):
            if widget.font().pointSize() == 32:
                widget.setText(self.value_text)


class ChartPanel(QFrame):
    """Professional chart visualization panel"""
    
    def __init__(self, title, chart_type="line"):
        super().__init__()
        self.title_text = title
        self.chart_type = chart_type
        self.init_ui()
        self.apply_styling()
        
    def init_ui(self):
        """Initialize chart panel"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Title
        title = QLabel(self.title_text)
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #ecf0f1; margin: 5px 0px;")
        layout.addWidget(separator)
        
        # Create chart
        self.chart = self.create_chart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.chart_view)
        
    def create_chart(self):
        """Create appropriate chart type"""
        chart = QChart()
        chart.setBackgroundBrush(QBrush(QColor(255, 255, 255)))
        chart.setTitleBrush(QBrush(QColor(44, 62, 80)))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        if self.chart_type == "line":
            series = QLineSeries()
            series.setName("Performance")
            
            # Generate sample data
            for i in range(12):
                series.append(i, random.randint(20, 100))
            
            chart.addSeries(series)
            
            # Axes
            axis_x = QValueAxis()
            axis_x.setLabelsVisible(True)
            axis_x.setTitleText("Time (Hours)")
            
            axis_y = QValueAxis()
            axis_y.setLabelsVisible(True)
            axis_y.setTitleText("Value (%)")
            
            chart.addAxis(axis_x, Qt.AlignBottom)
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)
            
        elif self.chart_type == "pie":
            pie_series = QPieSeries()
            slices_data = [("Operations", 35), ("Maintenance", 25), ("Development", 20), ("Support", 20)]
            
            for name, value in slices_data:
                slice_obj = pie_series.append(name, value)
                slice_obj.setLabelVisible(True)
            
            chart.addSeries(pie_series)
        
        return chart
        
    def apply_styling(self):
        """Apply panel styling"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            ChartPanel {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ecf0f1;
            }
        """)


class DataTablePanel(QFrame):
    """Professional data table panel"""
    
    def __init__(self, title):
        super().__init__()
        self.title_text = title
        self.init_ui()
        self.apply_styling()
        
    def init_ui(self):
        """Initialize table panel"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Title
        title = QLabel(self.title_text)
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #ecf0f1;")
        layout.addWidget(separator)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Status", "Progress", "Time"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ecf0f1;
                border: none;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #2c3e50;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #ecf0f1;
            }
        """)
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 100)
        
        # Sample data
        self.populate_table()
        layout.addWidget(self.table)
        
    def populate_table(self):
        """Populate table with sample data"""
        data = [
            ("001", "Active", 85),
            ("002", "Active", 72),
            ("003", "Idle", 45),
            ("004", "Active", 92),
            ("005", "Pending", 30),
        ]
        
        self.table.setRowCount(len(data))
        for row, (id_val, status, progress) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(id_val))
            self.table.setItem(row, 1, QTableWidgetItem(status))
            
            # Progress bar
            progress_bar = QProgressBar()
            progress_bar.setValue(progress)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 4px;
                    background-color: #ecf0f1;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #3498db;
                    border-radius: 4px;
                }
            """)
            self.table.setCellWidget(row, 2, progress_bar)
            
            # Time
            time_str = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
            self.table.setItem(row, 3, QTableWidgetItem(time_str))
        
        self.table.setRowHeight(0, 40)
        for i in range(1, len(data)):
            self.table.setRowHeight(i, 40)
    
    def apply_styling(self):
        """Apply panel styling"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            DataTablePanel {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ecf0f1;
            }
        """)


if QWebEnginePage is not None:
    class DebugWebPage(QWebEnginePage):
        """Subclass QWebEnginePage to capture console messages and forward them to the panel"""
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.owner = owner

        def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
            try:
                if hasattr(self.owner, 'status_label'):
                    # keep most recent console message visible for diagnostics
                    self.owner.status_label.setText(f"Console: {message}")
            except Exception:
                pass
            return super().javaScriptConsoleMessage(level, message, lineNumber, sourceID)
else:
    # Fallback stub when QWebEnginePage is unavailable
    class DebugWebPage(object):
        def __init__(self, owner, parent=None):
            self.owner = owner
        def __repr__(self):
            return "<DebugWebPage:stub>"

class VideoPanel(QFrame):
    """Panel to stream YouTube videos via QWebEngineView"""

    def __init__(self, title):
        super().__init__()
        self.title_text = title
        self.last_url = ''
        self.auto_open_on_fail = False
        self.init_ui()
        self.apply_styling()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title = QLabel(self.title_text)
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        # Controls
        control_layout = QHBoxLayout()
        self.url_input = ModernLineEdit("Enter YouTube URL or video id")
        control_layout.addWidget(self.url_input)

        load_btn = ModernPushButton("LOAD")
        load_btn.setMaximumWidth(120)
        load_btn.clicked.connect(self.load_from_input)
        control_layout.addWidget(load_btn)

        layout.addLayout(control_layout)

        # Web view (QWebEngineView may not be available in all environments)
        try:
            self.view = QWebEngineView()
            # Give it a minimum size so it is visible in the layout
            self.view.setMinimumHeight(360)
            layout.addWidget(self.view)

            # Status label and signals
            self.status_label = QLabel("")
            self.status_label.setFont(QFont("Segoe UI", 9))
            self.status_label.setStyleSheet("color: #7f8c8d; margin-top:6px;")
            layout.addWidget(self.status_label)

            # Use a debug page to capture console messages (if available)
            try:
                if QWebEnginePage is not None:
                    page = DebugWebPage(self, self.view)
                    self.view.setPage(page)
            except Exception:
                pass

            # Connect loading signals for progress and success/failure
            self.view.loadProgress.connect(self._on_load_progress)
            self.view.loadFinished.connect(self._on_load_finished)
            self.view.urlChanged.connect(lambda url: self.status_label.setText(url.toString()))

        except Exception as e:
            self.view = None
            error_label = QLabel("QWebEngineView unavailable: " + str(e))
            error_label.setStyleSheet("color: #c0392b;")
            layout.addWidget(error_label)

        # Sample buttons
        sample_layout = QHBoxLayout()
        samples = [
            ("Sample 1", "https://www.youtube.com/embed/dQw4w9WgXcQ"),
            ("Sample 2", "https://www.youtube.com/embed/9bZkp7q19f0"),
        ]
        for name, url in samples:
            btn = ModernPushButton(name, is_primary=False)
            btn.setMaximumWidth(120)
            btn.clicked.connect(lambda checked, u=url: self.load_url(u))
            sample_layout.addWidget(btn)

        # Auto-open toggle and Open in external browser button
        self.auto_open_chk = QCheckBox("Auto-open browser on load failure")
        self.auto_open_chk.setToolTip("If checked, the link will open in the external browser automatically when embedded playback fails.")
        sample_layout.addWidget(self.auto_open_chk)

        open_btn = ModernPushButton("Open in Browser", is_primary=False)
        open_btn.setMaximumWidth(160)
        open_btn.clicked.connect(self._open_in_browser)
        sample_layout.addWidget(open_btn)

        sample_layout.addStretch()
        layout.addLayout(sample_layout)

    def apply_styling(self):
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            VideoPanel {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ecf0f1;
            }
        """)

    def embed_url(self, url: str) -> str | None:
        """Normalize YouTube URL or ID to an embeddable URL."""
        if not url:
            return None
        u = url.strip()
        # already embed
        if "youtube.com/embed/" in u:
            return u
        # watch?v=...
        if "watch?v=" in u:
            vid = u.split("watch?v=")[1].split("&")[0]
            return f"https://www.youtube.com/embed/{vid}?autoplay=1"
        # youtu.be/...
        if "youtu.be/" in u:
            vid = u.split("youtu.be/")[1].split("?")[0]
            return f"https://www.youtube.com/embed/{vid}?autoplay=1"
        # plain id
        if len(u) <= 32 and '/' not in u and ' ' not in u:
            return f"https://www.youtube.com/embed/{u}?autoplay=1"
        # fallback
        return u

    def load_url(self, url: str):
        emb = self.embed_url(url)
        self.last_url = emb
        if not emb:
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid YouTube URL or video id (e.g. https://www.youtube.com/watch?v=VIDEO_ID or the short id).")
            return
        if not self.view:
            QMessageBox.critical(self, "No Web Engine", "QWebEngineView is unavailable in this environment.")
            return
        # start load
        try:
            self.status_label.setText("Starting load...")
        except Exception:
            pass
        self.view.setUrl(QUrl(emb))

    def load_from_input(self):
        url = self.url_input.text().strip()
        if url:
            self.load_url(url)

    def _on_load_progress(self, progress: int):
        try:
            self.status_label.setText(f"Loading... {progress}%")
        except Exception:
            pass

    def _on_load_finished(self, ok: bool):
        try:
            self.status_label.setText("Loaded" if ok else "Load failed")
        except Exception:
            pass
        if not ok:
            url = getattr(self, 'last_url', '') or (self.view.url().toString() if self.view else '')
            # Show diagnostic dialog with option to open externally
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Video Load Failed")
            msg.setText("Failed to load video. Possible causes: network, site blocking, unsupported embedded playback or missing codecs.")
            msg.setInformativeText(f"URL: {url}\n\nDo you want to open the link in your external browser instead?")
            open_btn = msg.addButton("Open in Browser", QMessageBox.AcceptRole)
            cancel_btn = msg.addButton(QMessageBox.Cancel)
            msg.exec()

            if msg.clickedButton() == open_btn:
                webbrowser.open(url)
                return

            # Auto-open if the checkbox is checked
            try:
                if getattr(self, 'auto_open_chk', None) and self.auto_open_chk.isChecked():
                    webbrowser.open(url)
                    return
            except Exception:
                pass

            # show helpful fallback HTML
            if self.view:
                html = "<html><body style='font-family:Arial;color:#2c3e50;'><h3>Unable to load video</h3><p>Check your network or try opening the link in your browser.</p></body></html>"
                self.view.setHtml(html)

    def _open_in_browser(self):
        url = getattr(self, 'last_url', '')
        if not url:
            url = self.url_input.text().strip()
        if url:
            webbrowser.open(url)
        else:
            QMessageBox.information(self, "No URL", "No video URL available to open.")


class ProfessionalLoginDialog(QDialog):
    """Premium login dialog with animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enterprise Dashboard Login")
        self.setFixedSize(500, 600)
        self.setModal(True)
        self.init_ui()
        self.apply_styling()
        
    def init_ui(self):
        """Initialize login UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo/Title Area
        logo_label = QLabel("🏢")
        logo_label.setFont(QFont("Arial", 64))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Company Name
        company = QLabel("Enterprise Solutions")
        company_font = QFont("Segoe UI", 22, QFont.Bold)
        company.setFont(company_font)
        company.setAlignment(Qt.AlignCenter)
        company.setStyleSheet("color: #2c3e50;")
        layout.addWidget(company)
        
        # Tagline
        tagline = QLabel("Advanced Analytics Dashboard")
        tagline_font = QFont("Segoe UI", 11)
        tagline.setFont(tagline_font)
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        layout.addWidget(tagline)
        
        # Username
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        username_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(username_label)
        
        self.username_input = ModernLineEdit("Enter your username")
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        password_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(password_label)
        
        self.password_input = ModernLineEdit("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(20)
        
        # Login Button
        login_btn = ModernPushButton("LOGIN")
        login_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        login_btn.clicked.connect(self.validate_login)
        layout.addWidget(login_btn)
        
        # Exit Button
        exit_btn = ModernPushButton("EXIT")
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #5d6d7b;
            }
        """)
        exit_btn.clicked.connect(self.reject)
        layout.addWidget(exit_btn)
        
        layout.addStretch()
        
        # Footer
        footer = QLabel("© 2025 Enterprise Solutions. All rights reserved.")
        footer.setFont(QFont("Segoe UI", 9))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #95a5a6; margin-top: 20px;")
        layout.addWidget(footer)
        
    def apply_styling(self):
        """Apply premium styling"""
        self.setStyleSheet("""
            ProfessionalLoginDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
            }
            QLineEdit {
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                padding: 10px;
                background-color: white;
                font-size: 12px;
                selection-background-color: #3498db;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #f8f9fa;
            }
        """)
        
    def validate_login(self):
        """Validate credentials"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Required", "Please enter both username and password")
            return
        
        if username == "admin" and password == "password":
            self.accept()
        else:
            QMessageBox.critical(self, "Authentication Failed", "Invalid credentials. Please try again.")
            self.password_input.clear()


class PIDSimulator:
    """Simple discrete-time PID controller and plant simulation for a cargo drone vertical axis"""
    def __init__(self, dt=0.02):
        self.dt = dt
        self.reset()

    def reset(self):
        self.t = 0.0
        self.y = 0.0  # altitude
        self.v = 0.0  # velocity
        self.integral = 0.0
        self.prev_error = 0.0
        self.data = []

    def step(self, setpoint, kp, ki, kd, mass=1.0, drag=0.1, thrust_limit=20.0):
        error = setpoint - self.y
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        u = kp * error + ki * self.integral + kd * derivative
        u = max(min(u, thrust_limit), -thrust_limit)
        # simple vertical dynamics: m * a = u - drag * v
        a = (u - drag * self.v) / mass
        self.v += a * self.dt
        self.y += self.v * self.dt
        self.t += self.dt
        self.prev_error = error
        self.data.append((self.t, self.y, self.v, u, error))
        return self.t, self.y, self.v, u, error


class PIDDashboard(QMainWindow):
    """Reimagined dashboard for PID tuning and simulation of a cargo drone"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cargo Drone PID Simulator")
        self.setGeometry(100, 50, 1200, 800)

        self.sim = PIDSimulator(dt=0.02)
        self.playing = False
        self.series_response = None
        self.series_setpoint = None

        self.init_ui()
        self.apply_styling()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("Cargo Drone PID Simulator")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        # Controls and plot area
        main_h = QHBoxLayout()
        controls = QVBoxLayout()
        controls.setSpacing(8)

        # PID controls
        self.kp_input = QLineEdit("1.0")
        self.ki_input = QLineEdit("0.0")
        self.kd_input = QLineEdit("0.0")
        self.setpoint_input = QLineEdit("10.0")
        form_rows = [
            ("Kp:", self.kp_input),
            ("Ki:", self.ki_input),
            ("Kd:", self.kd_input),
            ("Setpoint (m):", self.setpoint_input),
        ]
        for label, widget in form_rows:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            row.addWidget(widget)
            controls.addLayout(row)

        # Plant params
        self.mass_input = QLineEdit("1.0")
        self.drag_input = QLineEdit("0.1")
        row = QHBoxLayout()
        row.addWidget(QLabel("Mass (kg):"))
        row.addWidget(self.mass_input)
        controls.addLayout(row)
        row = QHBoxLayout()
        row.addWidget(QLabel("Drag coeff:"))
        row.addWidget(self.drag_input)
        controls.addLayout(row)

        # Simulation controls
        sim_btns = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_play)
        sim_btns.addWidget(self.start_btn)
        self.step_btn = QPushButton("Step")
        self.step_btn.clicked.connect(self.step_once)
        sim_btns.addWidget(self.step_btn)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_sim)
        sim_btns.addWidget(self.reset_btn)
        controls.addLayout(sim_btns)

        # Export
        self.export_btn = QPushButton("Export CSV")
        self.export_btn.clicked.connect(self.export_csv)
        controls.addWidget(self.export_btn)
        controls.addStretch()

        main_h.addLayout(controls, 0)

        # Plot using QtCharts
        chart = QChart()
        chart.setTitle("Altitude Response")
        axis_x = QValueAxis()
        axis_x.setTitleText("Time (s)")
        axis_y = QValueAxis()
        axis_y.setTitleText("Altitude (m)")
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)

        self.series_setpoint = QLineSeries()
        self.series_setpoint.setName("Setpoint")
        self.series_response = QLineSeries()
        self.series_response.setName("Response")
        chart.addSeries(self.series_setpoint)
        chart.addSeries(self.series_response)
        self.series_setpoint.attachAxis(axis_x)
        self.series_setpoint.attachAxis(axis_y)
        self.series_response.attachAxis(axis_x)
        self.series_response.attachAxis(axis_y)

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        main_h.addWidget(self.chart_view, 1)

        layout.addLayout(main_h)

        # Timer for playback
        self.timer = QTimer()
        self.timer.setInterval(int(self.sim.dt * 1000))
        self.timer.timeout.connect(self._simulate_step)

    def toggle_play(self):
        if self.playing:
            self.playing = False
            self.start_btn.setText("Start")
            self.timer.stop()
        else:
            self.playing = True
            self.start_btn.setText("Pause")
            self.timer.start()

    def step_once(self):
        self._simulate_step()

    def reset_sim(self):
        self.sim.reset()
        self.series_response.clear()
        self.series_setpoint.clear()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save simulation CSV", "pid_sim.csv", "CSV Files (*.csv)")
        if not path:
            return
        with open(path, 'w', newline='') as f:
            f.write('t,y,v,u,error\n')
            for t, y, v, u, e in self.sim.data:
                f.write(f"{t},{y},{v},{u},{e}\n")
        QMessageBox.information(self, "Exported", f"Simulation exported to: {path}")

    def _simulate_step(self):
        try:
            kp = float(self.kp_input.text())
            ki = float(self.ki_input.text())
            kd = float(self.kd_input.text())
            sp = float(self.setpoint_input.text())
            mass = float(self.mass_input.text())
            drag = float(self.drag_input.text())
        except Exception:
            QMessageBox.warning(self, "Invalid inputs", "Please ensure numeric values for all parameters.")
            self.toggle_play()
            return
        t, y, v, u, err = self.sim.step(sp, kp, ki, kd, mass=mass, drag=drag)
        self.series_response.append(t, y)
        self.series_setpoint.append(t, sp)
        # Keep chart ranges updated
        chart = self.chart_view.chart()
        chart.axisX().setRange(max(0, t - 10), t + 0.1)
        ymin = min([p.y() for p in self.series_response.pointsVector()] + [sp]) if self.series_response.count() else 0
        ymax = max([p.y() for p in self.series_response.pointsVector()] + [sp]) if self.series_response.count() else 1
        chart.axisY().setRange(ymin - 1, ymax + 1)

    def apply_styling(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f7f9fb; }
        """)

    def logout(self):
        self.close()
        new_dash = show_login()
        if new_dash is None:
            QApplication.quit()
        else:
            new_dash.show()

def show_login():
    """Display login and return dashboard instance or None"""
    login = ProfessionalLoginDialog()
    if login.exec() == QDialog.Accepted:
        dashboard = PIDDashboard()
        dashboard.show()
        return dashboard
    else:
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    dashboard = show_login()
    if dashboard:
        sys.exit(app.exec())
    else:
        sys.exit(0)
