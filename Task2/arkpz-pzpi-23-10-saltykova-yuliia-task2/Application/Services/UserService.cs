using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Application.Services
{
    public class UserService : IUserService
    {
        private readonly IUserRepository _userRepository;

        public UserService(IUserRepository userRepository)
        {
            _userRepository = userRepository;
        }

        // Профільні операції для користувача
        public async Task<UserProfileDto> GetMyProfileAsync(int userId)
        {
            var user = await _userRepository.GetUserByIdAsync(userId);
            if (user == null)
            {
                throw new Exception("Користувача не знайдено.");
            }

            // Оновлюємо останню активність
            await _userRepository.UpdateLastActivityAsync(userId, DateTime.UtcNow);

            return MapToUserProfileDto(user);
        }

        public async Task<UserProfileDto> UpdateMyProfileAsync(int userId, UpdateUserProfileDto updateDto)
        {
            var user = await _userRepository.GetUserByIdAsync(userId);
            if (user == null)
            {
                throw new Exception("Користувача не знайдено.");
            }

            if (user.IsBlocked)
            {
                throw new Exception("Ваш профіль заблоковано. Зверніться до адміністратора.");
            }

            // Оновлюємо дані
            if (!string.IsNullOrWhiteSpace(updateDto.Username))
            {
                user.Username = updateDto.Username;
            }

            if (updateDto.Bio != null)
            {
                user.Bio = updateDto.Bio;
            }

            if (updateDto.LastLatitude.HasValue)
            {
                user.LastLatitude = updateDto.LastLatitude;
            }

            if (updateDto.LastLongitude.HasValue)
            {
                user.LastLongitude = updateDto.LastLongitude;
            }

            user.LastActivity = DateTime.UtcNow;
            var updatedUser = await _userRepository.UpdateUserAsync(user);

            return MapToUserProfileDto(updatedUser);
        }

        public async Task<bool> DeleteMyProfileAsync(int userId)
        {
            var user = await _userRepository.GetUserByIdAsync(userId);
            if (user == null)
            {
                throw new Exception("Користувача не знайдено.");
            }

            return await _userRepository.DeleteUserAsync(userId);
        }

        // Адміністративні операції
        public async Task<UserStatisticsDto> GetUserStatisticsAsync()
        {
            var users = await _userRepository.GetAllUsersAsync();
            var now = DateTime.UtcNow;
            var thirtyDaysAgo = now.AddDays(-30);

            return new UserStatisticsDto
            {
                TotalUsers = users.Count,
                ActiveUsers = users.Count(u => u.LastActivity.HasValue && u.LastActivity.Value >= thirtyDaysAgo),
                BlockedUsers = users.Count(u => u.IsBlocked),
                TotalRegularUsers = users.Count(u => u.Role == UserRole.DogOwner),
                TotalAdmins = users.Count(u => u.Role == UserRole.Admin)
            };
        }

        public async Task<List<UserActivityDto>> GetAllUsersActivityAsync()
        {
            var users = await _userRepository.GetAllUsersAsync();
            return users.Select(u => MapToUserActivityDto(u)).ToList();
        }

        public async Task<UserActivityDto> GetUserActivityAsync(int userId)
        {
            var user = await _userRepository.GetUserByIdAsync(userId);
            if (user == null)
            {
                throw new Exception("Користувача не знайдено.");
            }

            return MapToUserActivityDto(user);
        }

        public async Task<bool> BlockUserAsync(int userId, string blockReason)
        {
            var user = await _userRepository.GetUserByIdAsync(userId);
            if (user == null)
            {
                throw new Exception("Користувача не знайдено.");
            }

            if (user.Role == UserRole.Admin)
            {
                throw new Exception("Не можна заблокувати адміністратора.");
            }

            user.IsBlocked = true;
            user.BlockReason = blockReason;
            await _userRepository.UpdateUserAsync(user);

            return true;
        }

        public async Task<bool> UnblockUserAsync(int userId)
        {
            var user = await _userRepository.GetUserByIdAsync(userId);
            if (user == null)
            {
                throw new Exception("Користувача не знайдено.");
            }

            user.IsBlocked = false;
            user.BlockReason = null;
            await _userRepository.UpdateUserAsync(user);

            return true;
        }

        // Маппінг
        private UserProfileDto MapToUserProfileDto(User user)
        {
            return new UserProfileDto
            {
                Id = user.Id,
                Username = user.Username,
                Email = user.Email,
                Bio = user.Bio,
                Role = user.Role,
                LastLatitude = user.LastLatitude,
                LastLongitude = user.LastLongitude,
                LastActivity = user.LastActivity,
                IsBlocked = user.IsBlocked,
                BlockReason = user.BlockReason
            };
        }

        private UserActivityDto MapToUserActivityDto(User user)
        {
            return new UserActivityDto
            {
                Id = user.Id,
                Username = user.Username,
                Email = user.Email,
                LastActivity = user.LastActivity,
                IsBlocked = user.IsBlocked,
                BlockReason = user.BlockReason
            };
        }
    }
}
