# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import render_template
from flask_babel import gettext as _

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.tasks.models import Task
from kadi.lib.tasks.models import TaskState

from .models import NotificationName


def create_notification_data(notification):
    """Create notification data suitable for presenting it to a client.

    :param notification: A :class:`.Notification` object to use for creating the
        notification data.
    :return: A tuple containing the title and the HTML body of the notification.
    """
    title = body = notification.name

    # Task status notifications.
    if notification.name == NotificationName.TASK_STATUS:
        task = Task.query.filter(Task.id == notification.data["task_id"]).first()

        # Default task status notifications.
        title = _("Task status")

        if task is None:
            body = _("Task no longer exists.")
            return title, body

        if task.state == TaskState.PENDING:
            body = _("Waiting for available resources...")
        elif task.state == TaskState.RUNNING:
            body = _("Task running...")
        elif task.state == TaskState.SUCCESS:
            body = _("Task succeeded.")
        elif task.state == TaskState.FAILURE:
            body = _("Task failed.")
        elif task.state == TaskState.REVOKED:
            body = _("Task revoked.")

        # Publish resource task.
        if task.name == const.TASK_PUBLISH_RESOURCE:
            title = _("Publish resource")

            if task.state == TaskState.RUNNING:
                body = render_template(
                    "notifications/publish_resource.html", progress=task.progress
                )
            elif task.state in {TaskState.SUCCESS, TaskState.FAILURE}:
                template = (
                    task.result.get("template") if task.result is not None else None
                )
                body = template if template is not None else _("Unexpected error.")

        # Check if the additional task notification metadata contains a custom title,
        # which overwrites previous values.
        task_meta = notification.data.get("task_meta")

        if isinstance(task_meta, dict) and "task_title" in task_meta:
            title = task_meta["task_title"]

        title = f"{title} ({task.pretty_state})"

    return title, body


def dismiss_notification(notification):
    """Dismiss a notification.

    If the notification is of type ``"task_status"``, the referenced task will be
    revoked as well.

    :param notification: The :class:`.Notification` to dismiss.
    """
    if notification.name == NotificationName.TASK_STATUS:
        task = Task.query.filter(Task.id == notification.data["task_id"]).first()

        if task is not None:
            task.revoke()

    db.session.delete(notification)
