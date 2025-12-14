using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;

namespace Application.Services
{
    public class NotificationService : INotificationService
    {
        private readonly INotificationRepository _notificationRepository;
        private readonly IDogRepository _dogRepository;

        public NotificationService(INotificationRepository notificationRepository, IDogRepository dogRepository)
        {
            _notificationRepository = notificationRepository;
            _dogRepository = dogRepository;
        }

        public async Task<IEnumerable<NotificationDto>> GetUserNotificationsAsync(int userId)
        {
            var notifications = await _notificationRepository.GetByUserIdAsync(userId);
            return notifications.Select(n => MapToDto(n));
        }

        public async Task<NotificationDto?> GetNotificationByIdAsync(int id)
        {
            var notification = await _notificationRepository.GetByIdAsync(id);
            return notification != null ? MapToDto(notification) : null;
        }

        public async Task<NotificationDto> CreateNotificationAsync(int userId, CreateNotificationDto dto)
        {
            var notification = new Notification
            {
                Title = dto.Title,
                Message = dto.Message,
                NotificationType = dto.NotificationType,
                RelatedEntityId = dto.RelatedEntityId,
                UserId = userId,
                CreatedAt = DateTime.UtcNow,
                IsRead = false
            };

            var createdNotification = await _notificationRepository.AddAsync(notification);
            return MapToDto(createdNotification);
        }

        public async Task MarkAsReadAsync(int id, int userId)
        {
            var notification = await _notificationRepository.GetByIdAsync(id);
            if (notification == null)
                throw new Exception("Уведомление не найдено");

            if (notification.UserId != userId)
                throw new UnauthorizedAccessException("У вас нет доступа к этому уведомлению");

            await _notificationRepository.MarkAsReadAsync(id);
        }

        public async Task MarkAllAsReadAsync(int userId)
        {
            await _notificationRepository.MarkAllAsReadAsync(userId);
        }

        public async Task<int> GetUnreadCountAsync(int userId)
        {
            return await _notificationRepository.GetUnreadCountAsync(userId);
        }

        public async Task DeleteNotificationAsync(int id, int userId)
        {
            var notification = await _notificationRepository.GetByIdAsync(id);
            if (notification == null)
                throw new Exception("Уведомление не найдено");

            if (notification.UserId != userId)
                throw new UnauthorizedAccessException("У вас нет доступа к этому уведомлению");

            await _notificationRepository.DeleteAsync(id);
        }

        public async Task<int> GetUserIdByDogIdAsync(int dogId)
        {
            var dog = await _dogRepository.GetByIdAsync(dogId);
            if (dog == null)
                return 0;

            return dog.OwnerId;
        }

        private NotificationDto MapToDto(Notification notification)
        {
            return new NotificationDto
            {
                Id = notification.Id,
                Title = notification.Title,
                Message = notification.Message,
                CreatedAt = notification.CreatedAt,
                IsRead = notification.IsRead,
                NotificationType = notification.NotificationType,
                RelatedEntityId = notification.RelatedEntityId
            };
        }
    }
}
