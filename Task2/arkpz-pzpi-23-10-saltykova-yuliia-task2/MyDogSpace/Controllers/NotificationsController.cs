using Application.Abstractions.Interfaces;
using Application.DTOs;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class NotificationsController : ControllerBase
{
    private readonly INotificationService _notificationService;

    public NotificationsController(INotificationService notificationService)
    {
        _notificationService = notificationService;
    }

    private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

    /// <summary>
    /// Получить все уведомления текущего пользователя
    /// </summary>
    [HttpGet]
    public async Task<IActionResult> GetMyNotifications()
    {
        try
        {
            var notifications = await _notificationService.GetUserNotificationsAsync(GetCurrentUserId());
            return Ok(notifications);
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /// <summary>
    /// Получить количество непрочитанных уведомлений
    /// </summary>
    [HttpGet("unread-count")]
    public async Task<IActionResult> GetUnreadCount()
    {
        try
        {
            var count = await _notificationService.GetUnreadCountAsync(GetCurrentUserId());
            return Ok(new { unreadCount = count });
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /// <summary>
    /// Получить уведомление по ID
    /// </summary>
    [HttpGet("{id}")]
    public async Task<IActionResult> GetNotification(int id)
    {
        try
        {
            var notification = await _notificationService.GetNotificationByIdAsync(id);
            if (notification == null)
                return NotFound(new { message = "Уведомление не найдено" });

            return Ok(notification);
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /// <summary>
    /// Создать новое уведомление (для административного использования и IoT устройств)
    /// Не требует авторизации для IoT устройств
    /// </summary>
    [HttpPost]
    [AllowAnonymous]  // Разрешить доступ без авторизации для IoT устройств
    public async Task<IActionResult> CreateNotification([FromBody] CreateNotificationDto dto)
    {
        try
        {
            // Если передан userId в контексте (авторизованный пользователь)
            var userIdClaim = User.FindFirstValue(ClaimTypes.NameIdentifier);
            int userId;

            if (!string.IsNullOrEmpty(userIdClaim) && int.TryParse(userIdClaim, out int parsedUserId))
            {
                // Авторизованный пользователь создает уведомление для себя
                userId = parsedUserId;
            }
            else if (dto.RelatedEntityId.HasValue)
            {
                // Для IoT устройств: используем RelatedEntityId как UserId
                // (предполагается, что это ID собаки, связанной с владельцем)
                // Получаем владельца собаки
                userId = await _notificationService.GetUserIdByDogIdAsync(dto.RelatedEntityId.Value);
                if (userId == 0)
                {
                    return BadRequest(new { message = "Не удалось определить пользователя для уведомления" });
                }
            }
            else
            {
                return Unauthorized(new { message = "Требуется авторизация или передача RelatedEntityId" });
            }

            var notification = await _notificationService.CreateNotificationAsync(userId, dto);
            return CreatedAtAction(nameof(GetNotification), new { id = notification.Id }, notification);
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /// <summary>
    /// Отметить уведомление как прочитанное
    /// </summary>
    [HttpPut("{id}/read")]
    public async Task<IActionResult> MarkAsRead(int id)
    {
        try
        {
            await _notificationService.MarkAsReadAsync(id, GetCurrentUserId());
            return Ok(new { message = "Уведомление отмечено как прочитанное" });
        }
        catch (UnauthorizedAccessException)
        {
            return Forbid();
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /// <summary>
    /// Отметить все уведомления как прочитанные
    /// </summary>
    [HttpPut("read-all")]
    public async Task<IActionResult> MarkAllAsRead()
    {
        try
        {
            await _notificationService.MarkAllAsReadAsync(GetCurrentUserId());
            return Ok(new { message = "Все уведомления отмечены как прочитанные" });
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /// <summary>
    /// Удалить уведомление
    /// </summary>
    [HttpDelete("{id}")]
    [Authorize]
    public async Task<IActionResult> DeleteNotification(int id)
    {
        try
        {
            await _notificationService.DeleteNotificationAsync(id, GetCurrentUserId());
            return Ok(new { message = "Уведомление удалено" });
        }
        catch (UnauthorizedAccessException)
        {
            return Forbid();
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /// <summary>
    /// Создать уведомление от IoT устройства (альтернативный эндпоинт)
    /// Для совместимости с IoT системой
    /// </summary>
    [HttpPost("iot-alert")]
    [AllowAnonymous]
    public async Task<IActionResult> CreateIoTAlert([FromBody] CreateIoTNotificationDto dto)
    {
        try
        {
            if (dto.DogId <= 0)
                return BadRequest(new { message = "Требуется valid DogId" });

            // Получаем владельца собаки
            var userId = await _notificationService.GetUserIdByDogIdAsync(dto.DogId);
            if (userId == 0)
                return BadRequest(new { message = "Собака не найдена" });

            var notificationDto = new CreateNotificationDto
            {
                Title = dto.Title,
                Message = dto.Message,
                NotificationType = dto.NotificationType,
                RelatedEntityId = dto.DogId
            };

            var notification = await _notificationService.CreateNotificationAsync(userId, notificationDto);
            return CreatedAtAction(nameof(GetNotification), new { id = notification.Id }, notification);
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }
}
