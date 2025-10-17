using Application.Abstractions.Interfaces;
using Entities.Models;
using Infrastructure;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

public class DogRepository : IDogRepository
{
    private readonly MyDbContext _context;

    public DogRepository(MyDbContext context)
    {
        _context = context;
    }

    public async Task<Dog?> GetByIdAsync(int dogId)
    {
        return await _context.Dogs.FindAsync(dogId);
    }

    public async Task<IEnumerable<Dog>> GetByOwnerIdAsync(int ownerId)
    {
        return await _context.Dogs
            .Where(d => d.OwnerId == ownerId)
            .ToListAsync();
    }

    public async Task<Dog> AddAsync(Dog dog)
    {
        _context.Dogs.Add(dog);
        await _context.SaveChangesAsync();
        return dog;
    }

    public async Task UpdateAsync(Dog dog)
    {
        _context.Dogs.Update(dog);
        await _context.SaveChangesAsync();
    }

    public async Task DeleteAsync(int dogId)
    {
        var dog = await GetByIdAsync(dogId);
        if (dog != null)
        {
            _context.Dogs.Remove(dog);
            await _context.SaveChangesAsync();
        }
    }
}
