using Entities.Models;

namespace Application.Abstractions.Interfaces
{
    public interface IPartnerRepository
    {
        Task<Partner?> GetByIdAsync(int partnerId);
        Task<IEnumerable<Partner>> GetAllAsync();
        Task<Partner> AddAsync(Partner partner);
        Task UpdateAsync(Partner partner);
        Task DeleteAsync(int partnerId);
    }
}
