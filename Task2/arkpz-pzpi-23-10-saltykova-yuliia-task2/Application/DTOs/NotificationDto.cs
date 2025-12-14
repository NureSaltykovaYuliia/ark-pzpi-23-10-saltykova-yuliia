using System;

namespace Application.DTOs
{
    public class NotificationDto
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Message { get; set; }
        public DateTime CreatedAt { get; set; }
        public bool IsRead { get; set; }
        public string NotificationType { get; set; }
        public int? RelatedEntityId { get; set; }
    }

    public class CreateNotificationDto
    {
        public string Title { get; set; }
        public string Message { get; set; }
        public string NotificationType { get; set; }
        public int? RelatedEntityId { get; set; }
    }

    public class CreateIoTNotificationDto
    {
        public string Title { get; set; }
        public string Message { get; set; }
        public string NotificationType { get; set; }
        public int DogId { get; set; }  // Требуется для определения владельца
    }
}
