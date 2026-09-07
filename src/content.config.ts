import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const recipes = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/recipes' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string(),
    videoUrl: z.string().optional(), // Reels, YouTube Shorts, or MP4 link
    prepTime: z.string(), // e.g. "10 mins"
    cookTime: z.string(), // e.g. "5 mins"
    totalTime: z.string(), // e.g. "15 mins"
    yield: z.string().default('2 servings'),
    servingsCount: z.number().default(2),
    calories: z.number().optional(),
    difficulty: z.enum(['Easy', 'Medium', 'Advanced']).default('Easy'),
    category: z.enum(['Toasts & Spreads', 'Teas & Sips', 'Brunch & Bakes', 'Quick Bites']),
    tags: z.array(z.string()).default([]),
    author: z.string().default('Tea & Toast Team'),
    featured: z.boolean().default(false),
    teaPairing: z.object({
      teaName: z.string(),
      description: z.string(),
      brewingNotes: z.string().optional(),
    }).optional(),
    ingredients: z.array(z.object({
      name: z.string(),
      amount: z.string(),
      unit: z.string().optional(),
      notes: z.string().optional(),
    })),
    instructions: z.array(z.object({
      step: z.number(),
      title: z.string().optional(),
      instruction: z.string(),
    })),
    tips: z.array(z.string()).default([]),
    nutrition: z.object({
      calories: z.string().optional(),
      protein: z.string().optional(),
      fat: z.string().optional(),
      carbs: z.string().optional(),
    }).optional(),
  }),
});

export const collections = { recipes };
