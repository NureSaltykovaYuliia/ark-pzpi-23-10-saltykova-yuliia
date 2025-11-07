using Application.Abstractions.Interfaces;
using Entities.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace MyDogSpace.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize(Roles = "Admin")]
    public class AdminCodesController : ControllerBase
    {
        private readonly IAdminCodeRepository _adminCodeRepository;

        public AdminCodesController(IAdminCodeRepository adminCodeRepository)
        {
            _adminCodeRepository = adminCodeRepository;
        }

        private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

        [HttpPost]
        public async Task<IActionResult> CreateAdminCode()
        {
            try
            {
                var adminCode = new AdminCode
                {
                    Code = GenerateUniqueCode(),
                    IsUsed = false,
                    CreatedAt = DateTime.UtcNow
                };

                var createdCode = await _adminCodeRepository.AddAsync(adminCode);
                return Ok(new { code = createdCode.Code, message = "Код адміністратора створено успішно" });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetAllAdminCodes()
        {
            try
            {
                var codes = await _adminCodeRepository.GetAllAsync();
                return Ok(codes);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpGet("unused")]
        public async Task<IActionResult> GetUnusedAdminCodes()
        {
            try
            {
                var codes = await _adminCodeRepository.GetUnusedAsync();
                return Ok(codes);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        // Публічний endpoint для створення першого коду адміністратора (тільки якщо кодів ще немає)
        [HttpPost("initialize")]
        [AllowAnonymous]
        public async Task<IActionResult> CreateFirstAdminCode()
        {
            try
            {
                var existingCodes = await _adminCodeRepository.GetAllAsync();
                if (existingCodes.Count > 0)
                {
                    return BadRequest(new { message = "Коди адміністратора вже існують. Використовуйте звичайний endpoint." });
                }

                var adminCode = new AdminCode
                {
                    Code = GenerateUniqueCode(),
                    IsUsed = false,
                    CreatedAt = DateTime.UtcNow
                };

                var createdCode = await _adminCodeRepository.AddAsync(adminCode);
                return Ok(new { code = createdCode.Code, message = "Перший код адміністратора створено успішно" });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        private string GenerateUniqueCode()
        {
            return Guid.NewGuid().ToString("N").Substring(0, 16).ToUpper();
        }
    }
}
