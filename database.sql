-- Run this in the Supabase SQL Editor to create your database table

CREATE TABLE public.predictions (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    birth_date date NOT NULL,
    birth_place jsonb NOT NULL,
    birth_time jsonb NOT NULL,
    prediction jsonb,
    status text NOT NULL DEFAULT 'processing',
    open_ai_model text,
    error_message text,
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Row Level Security is disabled by default so your anon/publishable key can insert and read data smoothly!

-- If you want to allow anonymous inserts (useful if your frontend talks directly to Supabase, but since we have a Node backend using the Service Key, we can just let the backend handle it).
