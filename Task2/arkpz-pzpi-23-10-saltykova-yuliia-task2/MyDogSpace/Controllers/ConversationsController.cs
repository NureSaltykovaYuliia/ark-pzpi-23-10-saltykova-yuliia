using Application.Abstractions.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class ConversationsController : ControllerBase
{
    private readonly IConversationService _conversationService;

    public ConversationsController(IConversationService conversationService)
    {
        _conversationService = conversationService;
    }

    private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

    [HttpGet]
    public async Task<IActionResult> GetMyConversations()
    {
        var conversations = await _conversationService.GetUserConversationsAsync(GetCurrentUserId());
        return Ok(conversations);
    }

    [HttpGet("{id}/messages")]
    public async Task<IActionResult> GetMessageHistory(int id)
    {
        var messages = await _conversationService.GetMessageHistoryAsync(id, count: 50);
        return Ok(messages);
    }
}