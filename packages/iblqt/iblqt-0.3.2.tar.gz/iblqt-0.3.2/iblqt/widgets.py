"""Graphical user interface components."""

from typing import Any

from qtpy.QtWidgets import (
    QPushButton,
    QStyledItemDelegate,
    QStyleOptionButton,
    QCheckBox,
    QStyle,
    QApplication,
    QStyleOptionViewItem,
)
from qtpy.QtCore import (
    Signal,
    Slot,
    Property,
    QRect,
    QEvent,
    QModelIndex,
    QAbstractItemModel,
)
from qtpy.QtGui import QPainter, QMouseEvent


class CheckBoxDelegate(QStyledItemDelegate):
    """
    A custom delegate for rendering checkboxes in a QTableView or similar widget.

    This delegate allows for the display and interaction with boolean data as checkboxes.
    """

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        """
        Paints the checkbox in the view.

        Parameters
        ----------
        painter : QPainter
            The painter used to draw the checkbox.
        option : QStyleOptionButton
            The style option containing the information needed for painting.
        index : QModelIndex
            The index of the item in the model.
        """
        super().paint(painter, option, index)
        control = QStyleOptionButton()
        control.rect = QRect(option.rect.topLeft(), QCheckBox().sizeHint())
        control.rect.moveCenter(option.rect.center())
        control.state = QStyle.State_On if index.data() is True else QStyle.State_Off
        QApplication.style().drawControl(
            QStyle.ControlElement.CE_CheckBox, control, painter
        )

    def displayText(self, value: Any, locale: Any) -> str:
        """
        Return an empty string to hide the text representation of the data.

        Parameters
        ----------
        value : Any
            The value to be displayed (not used).
        locale : Any
            The locale to be used (not used).

        Returns
        -------
        str
            An empty string.
        """
        return ''

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        """
        Handle user interaction with the checkbox.

        Parameters
        ----------
        event : QEvent
            The event that occurred (e.g., mouse click).
        model : QAbstractItemModel
            The model associated with the view.
        option : QStyleOptionViewItem
            The style option containing the information needed for handling the event.
        index : QModelIndex
            The index of the item in the model.

        Returns
        -------
        bool
            True if the event was handled, False otherwise.
        """
        if isinstance(event, QMouseEvent) and event.type() == QEvent.MouseButtonRelease:
            checkbox_rect = QRect(option.rect.topLeft(), QCheckBox().sizeHint())
            checkbox_rect.moveCenter(option.rect.center())
            if checkbox_rect.contains(event.pos()):
                model.setData(index, not model.data(index))
                event.accept()
                return True
        return super().editorEvent(event, model, option, index)


class StatefulButton(QPushButton):
    """A QPushButton that maintains an active/inactive state."""

    clickedWhileActive = Signal()  # type: Signal
    """Emitted when the button is clicked while it is in the active state."""

    clickedWhileInactive = Signal()  # type: Signal
    """Emitted when the button is clicked while it is in the inactive state."""

    stateChanged = Signal(bool)  # type: Signal
    """Emitted when the button's state has changed. The signal carries the new state 
    (True for active, False for inactive)."""

    def __init__(self, *args, active: bool = False, **kwargs):
        """Initialize the StatefulButton with the specified active state.

        Parameters
        ----------
        *args : tuple
            Positional arguments passed to QPushButton constructor.
        active : bool, optional
            Initial state of the button (default is False).
        **kwargs : dict
            Keyword arguments passed to QPushButton constructor.
        """
        super().__init__(*args, **kwargs)
        self._isActive = active
        self.clicked.connect(self._onClick)

    def getActive(self) -> bool:
        """Get the active state of the button.

        Returns
        -------
        bool
            True if the button is active, False otherwise.
        """
        return self._isActive

    @Slot(bool)
    def setActive(self, value: bool):
        """Set the active state of the button.

        Emits `stateChanged` if the state has changed.

        Parameters
        ----------
        value : bool
            The new active state of the button.
        """
        if self._isActive != value:
            self._isActive = value
            self.stateChanged.emit(self._isActive)

    active = Property(bool, fget=getActive, fset=setActive, notify=stateChanged)  # type: Property
    """The active state of the button."""

    @Slot()
    def _onClick(self):
        """Handle the button click event.

        Emits `clickedWhileActive` if the button is active,
        otherwise emits `clickedWhileInactive`.
        """
        if self._isActive:
            self.clickedWhileActive.emit()
        else:
            self.clickedWhileInactive.emit()
