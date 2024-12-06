from PySide6.QtCore import Qt as qt


class Qt:
    GlobalColor = qt.GlobalColor
    AspectRatioMode = qt.AspectRatioMode
    ColorScheme = qt.ColorScheme
    AlignmentFlag = qt.AlignmentFlag
    ApplicationAttribute = qt.ApplicationAttribute

    class FindChildOption:
        Recursively = qt.FindChildOption.FindChildrenRecursively
        ChildrenOnly = qt.FindChildOption.FindDirectChildrenOnly

    class MouseButton:
        Left = qt.MouseButton.LeftButton
        Right = qt.MouseButton.RightButton
        Middle = qt.MouseButton.MiddleButton

    class ContextMenuPolicy:
        No = qt.ContextMenuPolicy.NoContextMenu
        Default = qt.ContextMenuPolicy.DefaultContextMenu
        Actions = qt.ContextMenuPolicy.ActionsContextMenu
        Custom = qt.ContextMenuPolicy.CustomContextMenu
        Prevent = qt.ContextMenuPolicy.PreventContextMenu

    class LayoutDirection:
        LeftToRight = qt.LayoutDirection.LeftToRight
        RightToLeft = qt.LayoutDirection.RightToLeft
        Auto = qt.LayoutDirection.LayoutDirectionAuto

    class TextInteraction:
        SelectableByMouse = qt.TextInteractionFlag.TextSelectableByMouse
        Browser = qt.TextInteractionFlag.TextBrowserInteraction

    class TransformationMode:
        Smooth = qt.TransformationMode.SmoothTransformation
        Fast = qt.TransformationMode.FastTransformation

    class CursorShape:
        PointingHand = qt.CursorShape.PointingHandCursor
        IBeam = qt.CursorShape.IBeamCursor
        Wait = qt.CursorShape.WaitCursor

    class TextFlag:
        SingleLine = qt.TextFlag.TextSingleLine
        DontClip = qt.TextFlag.TextDontClip
        ExpandTabs = qt.TextFlag.TextExpandTabs
        ShowMnemonic = qt.TextFlag.TextShowMnemonic
        WordWrap = qt.TextFlag.TextWordWrap
        WrapAnywhere = qt.TextFlag.TextWrapAnywhere
        DontPrint = qt.TextFlag.TextDontPrint
        HideMnemonic = qt.TextFlag.TextHideMnemonic
        JustificationForced = qt.TextFlag.TextJustificationForced
        ForceLeftToRight = qt.TextFlag.TextForceLeftToRight
        ForceRightToLeft = qt.TextFlag.TextForceRightToLeft
        LongestVariant = qt.TextFlag.TextLongestVariant
        IncludeTrailingSpaces = qt.TextFlag.TextIncludeTrailingSpaces

    class SortOrder:
        Asc = qt.SortOrder.AscendingOrder
        Desc = qt.SortOrder.DescendingOrder

    class Alignment:
        Left = qt.AlignmentFlag.AlignLeft
        Right = qt.AlignmentFlag.AlignRight
        HCenter = qt.AlignmentFlag.AlignHCenter
        Justify = qt.AlignmentFlag.AlignJustify

        Top = qt.AlignmentFlag.AlignTop
        Bottom = qt.AlignmentFlag.AlignBottom
        VCenter = qt.AlignmentFlag.AlignVCenter
        Baseline = qt.AlignmentFlag.AlignBaseline

        Center = qt.AlignmentFlag.AlignCenter
        Absolute = qt.AlignmentFlag.AlignAbsolute

        HMask = qt.AlignmentFlag.AlignHorizontal_Mask
        VMask = qt.AlignmentFlag.AlignVertical_Mask

    class DataRole:
        Display = qt.ItemDataRole.DisplayRole
        Decoration = qt.ItemDataRole.DecorationRole
        Edit = qt.ItemDataRole.EditRole
        ToolTip = qt.ItemDataRole.ToolTipRole
        StatusTip = qt.ItemDataRole.StatusTipRole
        WhatsThis = qt.ItemDataRole.WhatsThisRole
        SizeHint = qt.ItemDataRole.SizeHintRole

        Font = qt.ItemDataRole.FontRole
        TextAlignment = qt.ItemDataRole.TextAlignmentRole
        Background = qt.ItemDataRole.BackgroundRole
        Foreground = qt.ItemDataRole.ForegroundRole
        CheckState = qt.ItemDataRole.CheckStateRole
        InitialSortOrder = qt.ItemDataRole.InitialSortOrderRole

        AccessibleText = qt.ItemDataRole.AccessibleTextRole
        AccessibleDescription = qt.ItemDataRole.AccessibleDescriptionRole

        User = qt.ItemDataRole.UserRole

    class Orientation:
        Hor = qt.Orientation.Horizontal
        Ver = qt.Orientation.Vertical

    class ScrollBarPolicy:
        Needed = qt.ScrollBarPolicy.ScrollBarAsNeeded
        Off = qt.ScrollBarPolicy.ScrollBarAlwaysOff
        On = qt.ScrollBarPolicy.ScrollBarAlwaysOn

    class ItemFlag:
        No = qt.ItemFlag.NoItemFlags
        Selectable = qt.ItemFlag.ItemIsSelectable
        Editable = qt.ItemFlag.ItemIsEditable
        DragEnabled = qt.ItemFlag.ItemIsDragEnabled
        DropEnabled = qt.ItemFlag.ItemIsDropEnabled
        UserCheckable = qt.ItemFlag.ItemIsUserCheckable
        Enabled = qt.ItemFlag.ItemIsEnabled
        NeverHasChildren = qt.ItemFlag.ItemNeverHasChildren
        UserTristate = qt.ItemFlag.ItemIsUserTristate
        AutoTristate = qt.ItemFlag.ItemIsAutoTristate

    class CheckState:
        Unchecked = qt.CheckState.Unchecked
        Partially = qt.CheckState.PartiallyChecked
        Checked = qt.CheckState.Checked

    class WidgetAttribute:
        DeleteOnClose = qt.WidgetAttribute.WA_DeleteOnClose
        StyledBackground = qt.WidgetAttribute.WA_StyledBackground
        Translucent = qt.WidgetAttribute.WA_TranslucentBackground

    class Key:
        B = qt.Key.Key_B
        Space = qt.Key.Key_Space
        Return = qt.Key.Key_Return
        Enter = qt.Key.Key_Enter
        Backspace = qt.Key.Key_Backspace
        Control = qt.Key.Key_Control
        Delete = qt.Key.Key_Delete

    class KeyboardModifier:
        No = qt.KeyboardModifier.NoModifier
        Control = qt.KeyboardModifier.ControlModifier

    class WindowType:
        Dialog = qt.WindowType.Dialog
        MinMaxButton = qt.WindowType.WindowMinMaxButtonsHint
        CloseButton = qt.WindowType.WindowCloseButtonHint
        Widget = qt.WindowType.Widget
        Title = qt.WindowType.WindowTitleHint
        Frameless = qt.WindowType.FramelessWindowHint
        Popup = qt.WindowType.Popup
        NoShadow = qt.WindowType.NoDropShadowWindowHint
