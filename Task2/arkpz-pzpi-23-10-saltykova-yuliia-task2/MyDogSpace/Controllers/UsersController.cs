using Application.Abstractions.Interfaces;
using Application.DTOs;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace MyDogSpace.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class UsersController : ControllerBase
    {
        private readonly IUserService _userService;

        public UsersController(IUserService userService)
        {
            _userService = userService;
        }

        private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

        private bool IsAdmin() => User.FindFirstValue(ClaimTypes.Role) == "Admin";

        // Користувацькі endpoints (доступні всім авторизованим користувачам)

      
        /// Отримати профіль поточного користувача
       
        [HttpGet("profile")]
        public async Task<IActionResult> GetMyProfile()
        {
            try
            {
                var profile = await _userService.GetMyProfileAsync(GetCurrentUserId());
                return Ok(profile);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

     
        /// Оновити профіль поточного користувача
     
        [HttpPut("profile")]
        public async Task<IActionResult> UpdateMyProfile([FromBody] UpdateUserProfileDto updateDto)
        {
            try
            {
                var updatedProfile = await _userService.UpdateMyProfileAsync(GetCurrentUserId(), updateDto);
                return Ok(updatedProfile);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

     
        /// Видалити профіль поточного користувача
    
        [HttpDelete("profile")]
        public async Task<IActionResult> DeleteMyProfile()
        {
            try
            {
                var result = await _userService.DeleteMyProfileAsync(GetCurrentUserId());
                if (result)
                {
                    return Ok(new { message = "Профіль успішно видалено." });
                }
                return BadRequest(new { message = "Не вдалося видалити профіль." });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        // Адміністративні endpoints (доступні тільки адміністраторам)


        /// Отримати загальну статистику користувачів (тільки для адміністраторів)

        [HttpGet("admin/statistics")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetUserStatistics()
        {
            try
            {
                var statistics = await _userService.GetUserStatisticsAsync();
                return Ok(statistics);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }


        /// Отримати статистику активності всіх користувачів (тільки для адміністраторів)

        [HttpGet("admin/activity")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetAllUsersActivity()
        {
            try
            {
                var activities = await _userService.GetAllUsersActivityAsync();
                return Ok(activities);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

     
        /// Отримати статистику активності конкретного користувача (тільки для адміністраторів)
    
        [HttpGet("admin/activity/{userId}")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetUserActivity(int userId)
        {
            try
            {
                var activity = await _userService.GetUserActivityAsync(userId);
                return Ok(activity);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

      
        /// Заблокувати користувача (тільки для адміністраторів)
      
        [HttpPost("admin/block/{userId}")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> BlockUser(int userId, [FromBody] BlockUserDto blockDto)
        {
            try
            {
                var result = await _userService.BlockUserAsync(userId, blockDto.BlockReason);
                if (result)
                {
                    return Ok(new { message = "Користувача заблоковано." });
                }
                return BadRequest(new { message = "Не вдалося заблокувати користувача." });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

       
        /// Розблокувати користувача (тільки для адміністраторів)
   
        [HttpPost("admin/unblock/{userId}")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> UnblockUser(int userId)
        {
            try
            {
                var result = await _userService.UnblockUserAsync(userId);
                if (result)
                {
                    return Ok(new { message = "Користувача розблоковано." });
                }
                return BadRequest(new { message = "Не вдалося розблокувати користувача." });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }
    }
}
