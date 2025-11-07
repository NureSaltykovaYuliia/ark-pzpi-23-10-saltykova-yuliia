using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;

namespace Application.Services
{
    public class PartnerService : IPartnerService
    {
        private readonly IPartnerRepository _partnerRepository;

        public PartnerService(IPartnerRepository partnerRepository)
        {
            _partnerRepository = partnerRepository;
        }

        public async Task<IEnumerable<PartnerDto>> GetAllPartnersAsync()
        {
            var partners = await _partnerRepository.GetAllAsync();
            return partners.Select(MapToDto);
        }

        public async Task<PartnerDto?> GetPartnerByIdAsync(int id)
        {
            var partner = await _partnerRepository.GetByIdAsync(id);
            if (partner == null) return null;

            return MapToDto(partner);
        }

        public async Task<PartnerDto> CreatePartnerAsync(CreateUpdatePartnerDto partnerDto)
        {
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
            return MapToDto(createdPartner);
        }

        public async Task UpdatePartnerAsync(int id, CreateUpdatePartnerDto partnerDto)
        {
            var partner = await _partnerRepository.GetByIdAsync(id);
            if (partner == null)
                throw new Exception("Партнер не знайдений");

            partner.Name = partnerDto.Name;
            partner.Description = partnerDto.Description;
            partner.Address = partnerDto.Address;
            partner.PhoneNumber = partnerDto.PhoneNumber;
            partner.Website = partnerDto.Website;
            partner.Latitude = partnerDto.Latitude;
            partner.Longitude = partnerDto.Longitude;

            await _partnerRepository.UpdateAsync(partner);
        }

        public async Task DeletePartnerAsync(int id)
        {
            var partner = await _partnerRepository.GetByIdAsync(id);
            if (partner == null)
                throw new Exception("Партнер не знайдений");

            await _partnerRepository.DeleteAsync(id);
        }

        private static PartnerDto MapToDto(Partner p)
        {
            return new PartnerDto
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Address = p.Address,
                PhoneNumber = p.PhoneNumber,
                Website = p.Website,
                Latitude = p.Latitude,
                Longitude = p.Longitude
            };
        }
    }
}
