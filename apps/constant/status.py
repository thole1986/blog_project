from flask_babel import lazy_gettext as _l

ACTIVE = 1
INACTIVE = 2
PENDING = 3
REMOVE = 4

ACTIVE_TEXT = _l('Đã kích hoạt')
INACTIVE_TEXT = _l('Chưa kích hoạt')
PENDING_TEXT = _l('Tạm ngưng')
REMOVE_TEXT = _l('Đã xoá')

STATUS_CHOICES = (
    (ACTIVE, ACTIVE_TEXT),
    (INACTIVE, INACTIVE_TEXT),
    (PENDING, PENDING_TEXT),
    (REMOVE, REMOVE_TEXT),
)
