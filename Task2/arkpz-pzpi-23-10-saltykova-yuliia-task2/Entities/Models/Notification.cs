using System;

namespace Entities.Models
{
    public class Notification
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Message { get; set; }
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public bool IsRead { get; set; } = false;

        // Связь: Кому отправлено? (Один-ко-многим)
        public int UserId { get; set; }
        public User User { get; set; }

        // Тип уведомления (например: "event", "message", "friend_request", "device_alert")
        public string NotificationType { get; set; }

        // Опциональная связь с сущностью, вызвавшей уведомление
        public int? RelatedEntityId { get; set; }
    }
}
