using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

[ApiController]
[Route("api/[controller]")]
[Authorize] 
public class DogsController : ControllerBase
{
    private readonly IDogRepository _dogRepository;

    public DogsController(IDogRepository dogRepository)
    {
        _dogRepository = dogRepository;
    }

    private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

   [HttpGet("my")]
    public async Task<IActionResult> GetMyDogs()
    {
        var dogs = await _dogRepository.GetByOwnerIdAsync(GetCurrentUserId());
        return Ok(dogs);
    }

   [HttpPost]
    public async Task<IActionResult> CreateDog([FromBody] CreateUpdateDogDto dogDto)
    {
        var dog = new Dog
        {
            Name = dogDto.Name,
            Breed = dogDto.Breed,
            DateOfBirth = dogDto.DateOfBirth,
            Description = dogDto.Description,
            OwnerId = GetCurrentUserId()
        };
        var createdDog = await _dogRepository.AddAsync(dog);
        return CreatedAtAction(nameof(GetDogById), new { id = createdDog.Id }, createdDog);
    }

    
    [HttpGet("{id}")]
    public async Task<IActionResult> GetDogById(int id)
    {
        var dog = await _dogRepository.GetByIdAsync(id);
        if (dog == null) return NotFound();
        if (dog.OwnerId != GetCurrentUserId()) return Forbid();
        return Ok(dog);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateDog(int id, [FromBody] CreateUpdateDogDto dogDto)
    {
        var dog = await _dogRepository.GetByIdAsync(id);
        if (dog == null) return NotFound();
        if (dog.OwnerId != GetCurrentUserId()) return Forbid();

        dog.Name = dogDto.Name;
        dog.Breed = dogDto.Breed;
        dog.DateOfBirth = dogDto.DateOfBirth;
        dog.Description = dogDto.Description;

        await _dogRepository.UpdateAsync(dog);
        return NoContent(); 
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteDog(int id)
    {
        var dog = await _dogRepository.GetByIdAsync(id);
        if (dog == null) return NotFound();
        if (dog.OwnerId != GetCurrentUserId()) return Forbid();

        await _dogRepository.DeleteAsync(id);
        return NoContent(); 
    }
}