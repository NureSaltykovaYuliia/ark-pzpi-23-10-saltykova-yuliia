using Application.Abstractions.Interfaces;
using Application.DTOs;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class DogsController : ControllerBase
{
    private readonly IDogService _dogService;

    public DogsController(IDogService dogService)
    {
        _dogService = dogService;
    }

    private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

    [HttpGet("my")]
    public async Task<IActionResult> GetMyDogs()
    {
        var dogs = await _dogService.GetDogsByOwnerIdAsync(GetCurrentUserId());
        return Ok(dogs);
    }

    [HttpPost]
    public async Task<IActionResult> CreateDog([FromBody] CreateUpdateDogDto dogDto)
    {
        try
        {
            var createdDog = await _dogService.CreateDogAsync(dogDto, GetCurrentUserId());
            return CreatedAtAction(nameof(GetDogById), new { id = createdDog.Id }, createdDog);
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetDogById(int id)
    {
        try
        {
            var dog = await _dogService.GetDogByIdAsync(id);
            if (dog == null) return NotFound();
            return Ok(dog);
        }
        catch (UnauthorizedAccessException)
        {
            return Forbid();
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateDog(int id, [FromBody] CreateUpdateDogDto dogDto)
    {
        try
        {
            await _dogService.UpdateDogAsync(id, dogDto, GetCurrentUserId());
            return NoContent();
        }
        catch (UnauthorizedAccessException)
        {
            return Forbid();
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteDog(int id)
    {
        try
        {
            await _dogService.DeleteDogAsync(id, GetCurrentUserId());
            return NoContent();
        }
        catch (UnauthorizedAccessException)
        {
            return Forbid();
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }
}