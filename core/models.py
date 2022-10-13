from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Match(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    mode = models.CharField(
        max_length=255,
        choices=(
            ("like", "like"),
            ("dislike", "dislike"),
        ),
        default="like",
    )
    is_matched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.by} (and) {self.to}"

    class Meta:
        unique_together = ("by", "to")
        verbose_name = "Match"
        verbose_name_plural = "Matches"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} sent to {self.receiver}"
