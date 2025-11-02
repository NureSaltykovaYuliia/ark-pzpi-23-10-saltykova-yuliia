using Entities.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class ConversationsController : ControllerBase
{
    private readonly IConversationRepository _convRepo;
    private readonly IMessageRepository _messageRepo;

    public ConversationsController(IConversationRepository convRepo, IMessageRepository messageRepo)
    {
        _convRepo = convRepo;
        _messageRepo = messageRepo;
    }

    private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

    [HttpGet]
    public async Task<IActionResult> GetMyConversations()
    {
        var conversations = await _convRepo.GetUserConversationsAsync(GetCurrentUserId());
        return Ok(conversations);
    }
    [HttpGet("{id}/messages")]
    public async Task<IActionResult> GetMessageHistory(int id)
    {
        var messages = await _messageRepo.GetMessagesAsync(id, count: 50); 
        return Ok(messages);
    }
}