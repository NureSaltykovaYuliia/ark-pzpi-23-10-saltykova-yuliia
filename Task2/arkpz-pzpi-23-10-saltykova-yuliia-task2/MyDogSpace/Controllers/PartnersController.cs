using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace MyDogSpace.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PartnersController : ControllerBase
    {
        private readonly IPartnerRepository _partnerRepository;

        public PartnersController(IPartnerRepository partnerRepository)
        {
            _partnerRepository = partnerRepository;
        }

        [HttpGet]
        public async Task<IActionResult> GetAllPartners()
        {
            var partners = await _partnerRepository.GetAllAsync();
            var partnerDtos = partners.Select(p => new PartnerDto
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Address = p.Address,
                PhoneNumber = p.PhoneNumber,
                Website = p.Website,
                Latitude = p.Latitude,
                Longitude = p.Longitude
            });
            return Ok(partnerDtos);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetPartnerById(int id)
        {
            var partner = await _partnerRepository.GetByIdAsync(id);
            if (partner == null) return NotFound();

            var partnerDto = new PartnerDto
            {
                Id = partner.Id,
                Name = partner.Name,
                Description = partner.Description,
                Address = partner.Address,
                PhoneNumber = partner.PhoneNumber,
                Website = partner.Website,
                Latitude = partner.Latitude,
                Longitude = partner.Longitude
            };
            return Ok(partnerDto);
        }

        [Authorize(Roles = "Admin,Business")]
        [HttpPost]
        public async Task<IActionResult> CreatePartner([FromBody] CreateUpdatePartnerDto partnerDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var partner = new Partner
            {
                Name = partnerDto.Name,
                Description = partnerDto.Description,
                Address = partnerDto.Address,
                PhoneNumber = partnerDto.PhoneNumber,
                Website = partnerDto.Website,
                Latitude = partnerDto.Latitude,
                Longitude = partnerDto.Longitude
            };

            var createdPartner = await _partnerRepository.AddAsync(partner);
            return CreatedAtAction(nameof(GetPartnerById), new { id = createdPartner.Id }, createdPartner);
        }

        [Authorize(Roles = "Admin,Business")]
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdatePartner(int id, [FromBody] CreateUpdatePartnerDto partnerDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var partner = await _partnerRepository.GetByIdAsync(id);
            if (partner == null) return NotFound();

            partner.Name = partnerDto.Name;
            partner.Description = partnerDto.Description;
            partner.Address = partnerDto.Address;
            partner.PhoneNumber = partnerDto.PhoneNumber;
            partner.Website = partnerDto.Website;
            partner.Latitude = partnerDto.Latitude;
            partner.Longitude = partnerDto.Longitude;

            await _partnerRepository.UpdateAsync(partner);
            return NoContent();
        }

        [Authorize(Roles = "Admin")]
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePartner(int id)
        {
            var partner = await _partnerRepository.GetByIdAsync(id);
            if (partner == null) return NotFound();

            await _partnerRepository.DeleteAsync(id);
            return NoContent();
        }
    }
}
