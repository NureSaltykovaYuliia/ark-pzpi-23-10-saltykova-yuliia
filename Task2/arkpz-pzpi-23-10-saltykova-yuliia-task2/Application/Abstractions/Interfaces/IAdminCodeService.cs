using Application.DTOs;

namespace Application.Abstractions.Interfaces
{
    public interface IAdminCodeService
    {
        Task<AdminCodeDto> CreateAdminCodeAsync();
        Task<IEnumerable<AdminCodeDto>> GetAllAdminCodesAsync();
        Task<IEnumerable<AdminCodeDto>> GetUnusedAdminCodesAsync();
        Task<AdminCodeDto> CreateFirstAdminCodeAsync();
    }
}
