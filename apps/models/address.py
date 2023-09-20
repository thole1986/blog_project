from datetime import datetime as dt
from apps import db


class Province(db.Document):
    name = db.StringField()
    unaccented_name = db.StringField()
    created_by = db.ReferenceField("User")
    updated_by = db.ReferenceField("User")
    created_at = db.DateTimeField(default=dt.now)
    updated_at = db.DateTimeField()

    def __repr__(self):
        return self.name

    @property
    def districts(self):
        return District.objects(province=self).order_by('name')


class District(db.Document):
    name = db.StringField()
    unaccented_name = db.StringField()
    province = db.ReferenceField('Province')
    created_by = db.ReferenceField("User")
    updated_by = db.ReferenceField("User")
    created_at = db.DateTimeField(default=dt.now)
    updated_at = db.DateTimeField()

    def __repr__(self):
        return self.name

    @property
    def wards(self):
        return Ward.objects(district=self).order_by('name')


class Ward(db.Document):
    name = db.StringField()
    unaccented_name = db.StringField()
    district = db.ReferenceField('District')
    created_by = db.ReferenceField("User")
    updated_by = db.ReferenceField("User")
    created_at = db.DateTimeField(default=dt.now)
    updated_at = db.DateTimeField()

    def __repr__(self):
        return self.name


def _get_reference_zone(**kwargs):
    result = {
        'province': None,
        'district': None,
        'ward': None,
    }
    if kwargs.get('province'):
        try:
            province = Province.objects.get(id=kwargs.get('province'))
            result['province'] = province
        except Exception:
            pass
    if kwargs.get('district'):
        try:
            district = District.objects.get(id=kwargs.get('district'))
            result['district'] = district
        except Exception:
            pass
    if kwargs.get('ward'):
        try:
            ward = Ward.objects.get(id=kwargs.get('ward'))
            result['ward'] = ward
        except Exception:
            pass
    return result


def _get_address(ref_obj):
    address_list = [ref_obj.address]
    if isinstance(ref_obj.ward, Ward):
        address_list.extend([ref_obj.ward.name, ref_obj.ward.district.name, ref_obj.ward.district.province.name])
    else:
        if isinstance(ref_obj.district, District):
            address_list.extend([ref_obj.district.name, ref_obj.district.province.name])
        else:
            if isinstance(ref_obj.province, Province):
                address_list.extend([ref_obj.province.name])
    return ", ".join(map(str, address_list))