using Application.Abstractions.Interfaces;
using Entities.Models;
using Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Repositories
{
    public class PartnerRepository : IPartnerRepository
    {
        private readonly MyDbContext _context;

        public PartnerRepository(MyDbContext context)
        {
            _context = context;
        }

        public async Task<Partner?> GetByIdAsync(int partnerId)
        {
            return await _context.Partners.FindAsync(partnerId);
        }

        public async Task<IEnumerable<Partner>> GetAllAsync()
        {
            return await _context.Partners.ToListAsync();
        }

        public async Task<Partner> AddAsync(Partner partner)
        {
            _context.Partners.Add(partner);
            await _context.SaveChangesAsync();
            return partner;
        }

        public async Task UpdateAsync(Partner partner)
        {
            _context.Partners.Update(partner);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(int partnerId)
        {
            var partner = await GetByIdAsync(partnerId);
            if (partner != null)
            {
                _context.Partners.Remove(partner);
                await _context.SaveChangesAsync();
            }
        }
    }
}
