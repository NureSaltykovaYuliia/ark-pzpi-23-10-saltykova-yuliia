using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Entities.Models;

namespace Application.Abstractions.Interfaces
{
    public interface IDogRepository
    {
        Task<Dog?> GetByIdAsync(int dogId);
        Task<IEnumerable<Dog>> GetByOwnerIdAsync(int ownerId);
        Task<Dog> AddAsync(Dog dog);
        Task UpdateAsync(Dog dog);
        Task DeleteAsync(int dogId);
    }
}
