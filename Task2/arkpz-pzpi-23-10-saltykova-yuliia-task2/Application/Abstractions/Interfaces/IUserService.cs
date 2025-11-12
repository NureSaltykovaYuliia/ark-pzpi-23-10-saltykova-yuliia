using Application.DTOs;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Application.Abstractions.Interfaces
{
    public interface IUserService
    {
        // Профільні операції для користувача
        Task<UserProfileDto> GetMyProfileAsync(int userId);
        Task<UserProfileDto> UpdateMyProfileAsync(int userId, UpdateUserProfileDto updateDto);
        Task<bool> DeleteMyProfileAsync(int userId);

        // Адміністративні операції
        Task<UserStatisticsDto> GetUserStatisticsAsync();
        Task<List<UserActivityDto>> GetAllUsersActivityAsync();
        Task<UserActivityDto> GetUserActivityAsync(int userId);
        Task<bool> BlockUserAsync(int userId, string blockReason);
        Task<bool> UnblockUserAsync(int userId);
    }
}
