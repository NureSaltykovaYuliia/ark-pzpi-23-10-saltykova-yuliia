using Microsoft.AspNetCore.SignalR;
using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Application.Abstractions.Interfaces;
using Entities.Models;

namespace MyDogSpace.Hubs
{
    [Authorize] 
    public class ChatHub : Hub
    {
        private readonly IMessageRepository _messageRepo;
        private readonly IConversationRepository _conversationRepo;

        public ChatHub(IMessageRepository messageRepo, IConversationRepository conversationRepo)
        {
            _messageRepo = messageRepo;
            _conversationRepo = conversationRepo;
        }
        public async Task SendMessage(int conversationId, string content)
        { 
            var senderId = int.Parse(Context.User.FindFirstValue(ClaimTypes.NameIdentifier));
            var conversation = await _conversationRepo.GetByIdAsync(conversationId);
            if (conversation == null || !conversation.Participants.Any(p => p.Id == senderId))
            {
                throw new HubException("Ви не є учасником цієї розмови.");
            }
            var message = new Message
            {
                SenderId = senderId,
                ConversationId = conversationId,
                Content = content,
                Timestamp = DateTime.UtcNow
            };
            var savedMessage = await _messageRepo.CreateMessageAsync(message);
            await Clients.Group(conversationId.ToString()).SendAsync("ReceiveMessage", savedMessage);
        }
        public override async Task OnConnectedAsync()
        {
            var userId = int.Parse(Context.User.FindFirstValue(ClaimTypes.NameIdentifier));
            var conversations = await _conversationRepo.GetUserConversationsAsync(userId);
            foreach (var conv in conversations)
            {
                await Groups.AddToGroupAsync(Context.ConnectionId, conv.Id.ToString());
            }
            await base.OnConnectedAsync();
        }
        public override async Task OnDisconnectedAsync(Exception? exception)
        {
            await base.OnDisconnectedAsync(exception);
        }
    }
}