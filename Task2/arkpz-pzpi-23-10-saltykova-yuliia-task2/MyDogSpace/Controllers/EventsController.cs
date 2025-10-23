using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace MyDogSpace.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class EventsController : ControllerBase
    {
        private readonly IEventRepository _eventRepository;

        public EventsController(IEventRepository eventRepository)
        {
            _eventRepository = eventRepository;
        }

        private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

        [HttpGet]
        public async Task<IActionResult> GetAllEvents()
        {
            var events = await _eventRepository.GetAllAsync();
            var eventDtos = events.Select(e => new EventDto
            {
                Id = e.Id,
                Name = e.Name,
                Description = e.Description,
                StartTime = e.StartTime,
                EndTime = e.EndTime,
                Type = e.Type.ToString(),
                Latitude = e.Latitude,
                Longitude = e.Longitude,
                OrganizerId = e.OrganizerId,
                OrganizerName = e.Organizer?.Username
            });
            return Ok(eventDtos);
        }

        [HttpGet("upcoming")]
        public async Task<IActionResult> GetUpcomingEvents()
        {
            var events = await _eventRepository.GetUpcomingEventsAsync();
            var eventDtos = events.Select(e => new EventDto
            {
                Id = e.Id,
                Name = e.Name,
                Description = e.Description,
                StartTime = e.StartTime,
                EndTime = e.EndTime,
                Type = e.Type.ToString(),
                Latitude = e.Latitude,
                Longitude = e.Longitude,
                OrganizerId = e.OrganizerId,
                OrganizerName = e.Organizer?.Username
            });
            return Ok(eventDtos);
        }

        [HttpGet("my")]
        public async Task<IActionResult> GetMyEvents()
        {
            var events = await _eventRepository.GetByOrganizerIdAsync(GetCurrentUserId());
            var eventDtos = events.Select(e => new EventDto
            {
                Id = e.Id,
                Name = e.Name,
                Description = e.Description,
                StartTime = e.StartTime,
                EndTime = e.EndTime,
                Type = e.Type.ToString(),
                Latitude = e.Latitude,
                Longitude = e.Longitude,
                OrganizerId = e.OrganizerId,
                OrganizerName = e.Organizer?.Username
            });
            return Ok(eventDtos);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetEventById(int id)
        {
            var eventEntity = await _eventRepository.GetByIdAsync(id);
            if (eventEntity == null) return NotFound();

            var eventDto = new EventDto
            {
                Id = eventEntity.Id,
                Name = eventEntity.Name,
                Description = eventEntity.Description,
                StartTime = eventEntity.StartTime,
                EndTime = eventEntity.EndTime,
                Type = eventEntity.Type.ToString(),
                Latitude = eventEntity.Latitude,
                Longitude = eventEntity.Longitude,
                OrganizerId = eventEntity.OrganizerId,
                OrganizerName = eventEntity.Organizer?.Username
            };
            return Ok(eventDto);
        }

        [HttpPost]
        public async Task<IActionResult> CreateEvent([FromBody] CreateUpdateEventDto eventDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var eventEntity = new Event
            {
                Name = eventDto.Name,
                Description = eventDto.Description,
                StartTime = eventDto.StartTime,
                EndTime = eventDto.EndTime,
                Type = eventDto.Type,
                Latitude = eventDto.Latitude,
                Longitude = eventDto.Longitude,
                OrganizerId = GetCurrentUserId()
            };

            var createdEvent = await _eventRepository.AddAsync(eventEntity);
            return CreatedAtAction(nameof(GetEventById), new { id = createdEvent.Id }, createdEvent);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateEvent(int id, [FromBody] CreateUpdateEventDto eventDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var eventEntity = await _eventRepository.GetByIdAsync(id);
            if (eventEntity == null) return NotFound();
            if (eventEntity.OrganizerId != GetCurrentUserId()) return Forbid();

            eventEntity.Name = eventDto.Name;
            eventEntity.Description = eventDto.Description;
            eventEntity.StartTime = eventDto.StartTime;
            eventEntity.EndTime = eventDto.EndTime;
            eventEntity.Type = eventDto.Type;
            eventEntity.Latitude = eventDto.Latitude;
            eventEntity.Longitude = eventDto.Longitude;

            await _eventRepository.UpdateAsync(eventEntity);
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteEvent(int id)
        {
            var eventEntity = await _eventRepository.GetByIdAsync(id);
            if (eventEntity == null) return NotFound();
            if (eventEntity.OrganizerId != GetCurrentUserId()) return Forbid();

            await _eventRepository.DeleteAsync(id);
            return NoContent();
        }
    }
}
