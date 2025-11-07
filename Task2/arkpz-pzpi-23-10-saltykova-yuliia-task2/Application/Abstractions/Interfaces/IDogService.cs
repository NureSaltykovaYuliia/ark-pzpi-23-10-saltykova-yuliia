using Application.DTOs;

namespace Application.Abstractions.Interfaces
{
    public interface IDogService
    {
        Task<IEnumerable<DogDto>> GetDogsByOwnerIdAsync(int ownerId);
        Task<DogDto?> GetDogByIdAsync(int id);
        Task<DogDto> CreateDogAsync(CreateUpdateDogDto dogDto, int ownerId);
        Task UpdateDogAsync(int id, CreateUpdateDogDto dogDto, int ownerId);
        Task DeleteDogAsync(int id, int ownerId);
    }
}
