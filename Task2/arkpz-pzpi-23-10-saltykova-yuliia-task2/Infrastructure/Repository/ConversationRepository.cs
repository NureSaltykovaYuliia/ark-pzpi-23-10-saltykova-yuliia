using Application.Abstractions.Interfaces;
using Entities.Models;
using Infrastructure; 
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Infrastructure.Repositories
{
    public class ConversationRepository : IConversationRepository
    {
        private readonly MyDbContext _context;

        public ConversationRepository(MyDbContext context)
        {
            _context = context;
        }

        public async Task<Conversation> CreateConversationAsync(Conversation conversation)
        {
            await _context.Conversations.AddAsync(conversation);
            await _context.SaveChangesAsync();
            return conversation;
        }

        public async Task<Conversation?> FindPrivateConversationAsync(int user1Id, int user2Id)
        {
            // Шукаємо розмову, де є ТІЛЬКИ ці два учасники
            return await _context.Conversations
                .Include(c => c.Participants)
                .Where(c => c.Participants.Count == 2 &&
                            c.Participants.Any(p => p.Id == user1Id) &&
                            c.Participants.Any(p => p.Id == user2Id))
                .FirstOrDefaultAsync();
        }

        public async Task<Conversation?> GetByIdAsync(int conversationId)
        {
            // Дуже важливо завантажити учасників (Participants)
            // Це потрібно для ChatHub, щоб перевірити, чи є користувач у чаті
            return await _context.Conversations
                .Include(c => c.Participants)
                .FirstOrDefaultAsync(c => c.Id == conversationId);
        }

        public async Task<IEnumerable<Conversation>> GetUserConversationsAsync(int userId)
        {
            // Знаходимо всі розмови, де користувач є учасником
            return await _context.Conversations
                .Include(c => c.Participants) // Включаємо учасників, щоб показати, з ким чат
                .Where(c => c.Participants.Any(p => p.Id == userId))
                .ToListAsync();
        }
    }
}