# django-user-notifications
django-user-notifications is an extention of django-user-messages that extends the default django.contrib.messages framework.

The goal of the project is for a developer to create user messages with a set of rules.

Eg. You need a user to accept new terms of service for your site. You should be able to create that notification every day, every hour, every login until they accept the terms for which the notification will cease to appear. 

## Features
- Create per site and or per user messages
- Create messages based on schedule, login, and or views.
- Dismiss messages after user confirmation or end date.
- Automate message creation upon defined events.
- Select between modals or tranditional bootstrap notifications to display your message.

