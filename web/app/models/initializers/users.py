from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.users import Role
from flask import current_app


def add_initial_roles_to_database():

    try:
        user_role = Role(name='user', description="Application users")
        super_user_role = Role(name='superuser', description="Application superusers")
        no_ads_role = Role(name='no_ads', description="Won't display ads")
        basic_role = Role(name='basic', description="Basic users")
        pro_role = Role(name='pro', description="Pro users")
        enterprise_role = Role(name='enterprise', description="Enterprise users")

        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.add(no_ads_role)
        db.session.add(basic_role)
        db.session.add(pro_role)
        db.session.add(enterprise_role)
        db.session.commit()
    except IntegrityError as error:
        current_app.logger.debug("Role already exists: %s" % error)
