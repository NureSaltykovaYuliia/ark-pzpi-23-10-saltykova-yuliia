using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;

namespace Application.Services
{
    public class DogService : IDogService
    {
        private readonly IDogRepository _dogRepository;

        public DogService(IDogRepository dogRepository)
        {
            _dogRepository = dogRepository;
        }

        public async Task<IEnumerable<DogDto>> GetDogsByOwnerIdAsync(int ownerId)
        {
            var dogs = await _dogRepository.GetByOwnerIdAsync(ownerId);
            return dogs.Select(d => new DogDto
            {
                Id = d.Id,
                Name = d.Name,
                Breed = d.Breed,
                DateOfBirth = d.DateOfBirth,
                Description = d.Description
            });
        }

        public async Task<DogDto?> GetDogByIdAsync(int id)
        {
            var dog = await _dogRepository.GetByIdAsync(id);
            if (dog == null) return null;

            return new DogDto
            {
                Id = dog.Id,
                Name = dog.Name,
                Breed = dog.Breed,
                DateOfBirth = dog.DateOfBirth,
                Description = dog.Description
            };
        }

        public async Task<DogDto> CreateDogAsync(CreateUpdateDogDto dogDto, int ownerId)
        {
            var dog = new Dog
            {
                Name = dogDto.Name,
                Breed = dogDto.Breed,
                DateOfBirth = dogDto.DateOfBirth,
                Description = dogDto.Description,
                OwnerId = ownerId
            };

            var createdDog = await _dogRepository.AddAsync(dog);

            return new DogDto
            {
                Id = createdDog.Id,
                Name = createdDog.Name,
                Breed = createdDog.Breed,
                DateOfBirth = createdDog.DateOfBirth,
                Description = createdDog.Description
            };
        }

        public async Task UpdateDogAsync(int id, CreateUpdateDogDto dogDto, int ownerId)
        {
            var dog = await _dogRepository.GetByIdAsync(id);
            if (dog == null)
                throw new Exception("Собака не знайдена");

            if (dog.OwnerId != ownerId)
                throw new UnauthorizedAccessException("Ви не маєте доступу до цієї собаки");

            dog.Name = dogDto.Name;
            dog.Breed = dogDto.Breed;
            dog.DateOfBirth = dogDto.DateOfBirth;
            dog.Description = dogDto.Description;

            await _dogRepository.UpdateAsync(dog);
        }

        public async Task DeleteDogAsync(int id, int ownerId)
        {
            var dog = await _dogRepository.GetByIdAsync(id);
            if (dog == null)
                throw new Exception("Собака не знайдена");

            if (dog.OwnerId != ownerId)
                throw new UnauthorizedAccessException("Ви не маєте доступу до цієї собаки");

            await _dogRepository.DeleteAsync(id);
        }
    }
}
