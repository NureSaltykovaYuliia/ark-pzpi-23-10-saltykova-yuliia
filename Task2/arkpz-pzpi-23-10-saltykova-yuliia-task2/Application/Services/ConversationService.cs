using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;

namespace Application.Services
{
    public class ConversationService : IConversationService
    {
        private readonly IConversationRepository _conversationRepository;
        private readonly IMessageRepository _messageRepository;

        public ConversationService(IConversationRepository conversationRepository, IMessageRepository messageRepository)
        {
            _conversationRepository = conversationRepository;
            _messageRepository = messageRepository;
        }

        public async Task<IEnumerable<ConversationDto>> GetUserConversationsAsync(int userId)
        {
            var conversations = await _conversationRepository.GetUserConversationsAsync(userId);
            return conversations.Select(c => new ConversationDto
            {
                Id = c.Id,
                Name = c.Name,
                ParticipantIds = c.Participants?.Select(p => p.Id).ToList() ?? new List<int>(),
                ParticipantNames = c.Participants?.Select(p => p.Username).ToList() ?? new List<string>()
            });
        }

        public async Task<IEnumerable<MessageDto>> GetMessageHistoryAsync(int conversationId, int count = 50)
        {
            var messages = await _messageRepository.GetMessagesAsync(conversationId, count);
            return messages.Select(m => new MessageDto
            {
                Id = m.Id,
                Content = m.Content,
                Timestamp = m.Timestamp,
                SenderId = m.SenderId,
                SenderName = m.Sender?.Username ?? "Unknown",
                ConversationId = m.ConversationId
            });
        }
    }
}
