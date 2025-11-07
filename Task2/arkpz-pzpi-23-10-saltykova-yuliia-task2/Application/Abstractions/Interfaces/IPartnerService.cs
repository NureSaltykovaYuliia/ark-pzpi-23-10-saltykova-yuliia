using Application.DTOs;

namespace Application.Abstractions.Interfaces
{
    public interface IPartnerService
    {
        Task<IEnumerable<PartnerDto>> GetAllPartnersAsync();
        Task<PartnerDto?> GetPartnerByIdAsync(int id);
        Task<PartnerDto> CreatePartnerAsync(CreateUpdatePartnerDto partnerDto);
        Task UpdatePartnerAsync(int id, CreateUpdatePartnerDto partnerDto);
        Task DeletePartnerAsync(int id);
    }
}
