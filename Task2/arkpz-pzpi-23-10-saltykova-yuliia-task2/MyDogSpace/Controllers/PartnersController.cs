using Application.Abstractions.Interfaces;
using Application.DTOs;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace MyDogSpace.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PartnersController : ControllerBase
    {
        private readonly IPartnerService _partnerService;

        public PartnersController(IPartnerService partnerService)
        {
            _partnerService = partnerService;
        }

        [HttpGet]
        public async Task<IActionResult> GetAllPartners()
        {
            var partners = await _partnerService.GetAllPartnersAsync();
            return Ok(partners);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetPartnerById(int id)
        {
            var partner = await _partnerService.GetPartnerByIdAsync(id);
            if (partner == null) return NotFound();
            return Ok(partner);
        }

        [Authorize(Roles = "Admin")]
        [HttpPost]
        public async Task<IActionResult> CreatePartner([FromBody] CreateUpdatePartnerDto partnerDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            try
            {
                var createdPartner = await _partnerService.CreatePartnerAsync(partnerDto);
                return CreatedAtAction(nameof(GetPartnerById), new { id = createdPartner.Id }, createdPartner);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [Authorize(Roles = "Admin")]
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdatePartner(int id, [FromBody] CreateUpdatePartnerDto partnerDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            try
            {
                await _partnerService.UpdatePartnerAsync(id, partnerDto);
                return NoContent();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [Authorize(Roles = "Admin")]
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePartner(int id)
        {
            try
            {
                await _partnerService.DeletePartnerAsync(id);
                return NoContent();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }
    }
}
