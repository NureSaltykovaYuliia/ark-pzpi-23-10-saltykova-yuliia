using Application.Abstractions.Interfaces;
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
        private readonly IAdminCodeService _adminCodeService;

        public AdminCodesController(IAdminCodeService adminCodeService)
        {
            _adminCodeService = adminCodeService;
        }

        private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

        [HttpPost]
        public async Task<IActionResult> CreateAdminCode()
        {
            try
            {
                var createdCode = await _adminCodeService.CreateAdminCodeAsync();
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
                var codes = await _adminCodeService.GetAllAdminCodesAsync();
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
                var codes = await _adminCodeService.GetUnusedAdminCodesAsync();
                return Ok(codes);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("initialize")]
        [AllowAnonymous]
        public async Task<IActionResult> CreateFirstAdminCode()
        {
            try
            {
                var createdCode = await _adminCodeService.CreateFirstAdminCodeAsync();
                return Ok(new { code = createdCode.Code, message = "Перший код адміністратора створено успішно" });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }
    }
}
