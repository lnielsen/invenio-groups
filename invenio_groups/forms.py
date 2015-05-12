# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Group Forms."""


from __future__ import absolute_import, print_function, unicode_literals

from sqlalchemy_utils.types.choice import ChoiceType
from wtforms import RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, StopValidation, \
    ValidationError
from wtforms_alchemy import ClassMap, model_form_factory

from invenio.base.i18n import _
from invenio.utils.forms import InvenioBaseForm

from .models import Group

ModelForm = model_form_factory(InvenioBaseForm)


class EmailsValidator(object):

    """."""

    def __init__(self):
        """."""
        self.validate_data = DataRequired()
        self.validate_email = Email()

    def __call__(self, form, field):
        """."""
        self.validate_data(form, field)

        emails_org = field.data
        emails = filter(None, emails_org.splitlines())
        for email in emails:
            try:
                field.data = email
                self.validate_email(form, field)
            except (ValidationError, StopValidation):
                raise ValidationError('Invalid email: ' + email)
            finally:
                field.data = emails_org


class GroupForm(ModelForm):

    """New group form."""

    class Meta:
        model = Group
        type_map = ClassMap({ChoiceType: RadioField})
        exclude = [
            'is_managed',
        ]


class NewMemberForm(InvenioBaseForm):

    """Select a user that Join an existing group."""

    emails = TextAreaField(
        description=_(
            'Required. Provide list of the emails of the users'
            ' you wish to be added. Put each email in new line.'),
        validators=[EmailsValidator()]
    )
