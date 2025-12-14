using Application.DTOs;

namespace Application.Abstractions.Interfaces
{
    public interface INotificationService
    {
        Task<IEnumerable<NotificationDto>> GetUserNotificationsAsync(int userId);
        Task<NotificationDto?> GetNotificationByIdAsync(int id);
        Task<NotificationDto> CreateNotificationAsync(int userId, CreateNotificationDto dto);
        Task MarkAsReadAsync(int id, int userId);
        Task MarkAllAsReadAsync(int userId);
        Task<int> GetUnreadCountAsync(int userId);
        Task DeleteNotificationAsync(int id, int userId);
        Task<int> GetUserIdByDogIdAsync(int dogId);
    }
}
