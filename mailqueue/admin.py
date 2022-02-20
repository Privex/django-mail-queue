from django.contrib import admin, messages
from django.contrib.messages import add_message
from django.utils.translation import gettext_lazy as _

from .models import MailerMessage, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class MailerAdmin(admin.ModelAdmin):
    list_display = ('created', 'subject', 'to_address', 'app', 'sent', 'last_attempt', 'reply_to')
    search_fields = ['to_address', 'subject', 'app', 'cc_address', 'bcc_address', 'reply_to']
    actions = ['send_failed', 'resend_emails', 'mark_unsent']
    inlines = [AttachmentInline]
    date_hierarchy = "created"

    def resend_emails(self, request, queryset):
        for m in queryset:  # type: MailerMessage
            m.sent = False
            m.save()
            m.send_mail()
            add_message(request, messages.SUCCESS,
                        "Resent Message ID {} (Subj: {})".format(m.id, m.subject))

    resend_emails.short_description = _("(Re-)send emails immediately")

    def mark_unsent(self, request, queryset):
        for m in queryset:  # type: MailerMessage
            m.sent = False
            m.save()
            add_message(request, messages.SUCCESS,
                        "Marked message ID {} (Subj: {}) as NOT sent".format(m.id, m.subject))

    mark_unsent.short_description = _("Mark emails as un-sent (re-send them via queue)")

    def send_failed(self, request, queryset):
        emails = queryset.filter(sent=False)
        for email in emails:
            email.send_mail()
        self.message_user(request, _("Emails queued."))

    send_failed.short_description = _("Send failed")


admin.site.register(MailerMessage, MailerAdmin)
