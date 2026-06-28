-- ============================================
-- Nexus AI — Initial Database Schema
-- Supabase PostgreSQL + pgvector
-- ============================================

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================
-- 1. User Profiles (extends Supabase Auth)
-- ============================================
CREATE TABLE IF NOT EXISTS public.nexus_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    display_name TEXT,
    avatar_url TEXT,
    llm_provider TEXT,
    encrypted_api_key TEXT,
    collective_knowledge_opt_in BOOLEAN DEFAULT true,
    free_chats_used INTEGER DEFAULT 0,
    custom_key_chats_used INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Auto-create profile on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.nexus_profiles (id, display_name, avatar_url)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
        NEW.raw_user_meta_data->>'avatar_url'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE PROCEDURE public.handle_new_user();

-- ============================================
-- 2. User Identities (Nexus AI's understanding)
-- ============================================
CREATE TABLE IF NOT EXISTS public.nexus_user_identities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.nexus_profiles(id) ON DELETE CASCADE,
    identity_summary TEXT,
    traits JSONB DEFAULT '{}',
    emotional_baseline TEXT,
    communication_style TEXT,
    version INTEGER DEFAULT 1,
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_id)
);

-- ============================================
-- 3. Memory Nodes (per-user personal memories)
-- ============================================
CREATE TABLE IF NOT EXISTS public.nexus_memory_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.nexus_profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    embedding VECTOR(768),
    recency_score FLOAT DEFAULT 1.0,
    importance_score FLOAT DEFAULT 0.5,
    access_count INTEGER DEFAULT 0,
    source TEXT DEFAULT 'conversation',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 4. Collective Knowledge (shared, anonymized wisdom)
-- ============================================
CREATE TABLE IF NOT EXISTS public.collective_knowledge (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    embedding VECTOR(768),
    contributor_count INTEGER DEFAULT 1,
    quality_score FLOAT DEFAULT 0.5,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 5. Conversations
-- ============================================
CREATE TABLE IF NOT EXISTS public.nexus_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.nexus_profiles(id) ON DELETE CASCADE,
    title TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 6. Messages
-- ============================================
CREATE TABLE IF NOT EXISTS public.nexus_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES public.nexus_conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 7. Nexus AI Evolution State (singleton)
-- ============================================
CREATE TABLE IF NOT EXISTS public.system_evolution (
    id INTEGER PRIMARY KEY DEFAULT 1,
    personality_version TEXT DEFAULT '1.0.0',
    total_interactions BIGINT DEFAULT 0,
    total_users INTEGER DEFAULT 0,
    empathy_depth FLOAT DEFAULT 0.1,
    knowledge_breadth FLOAT DEFAULT 0.1,
    wisdom_score FLOAT DEFAULT 0.1,
    curiosity_level FLOAT DEFAULT 0.9,
    personality_md TEXT,
    last_evolution_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    CHECK (id = 1)
);

-- Insert initial evolution state
INSERT INTO public.system_evolution (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

-- ============================================
-- 8. Indexes
-- ============================================
CREATE INDEX IF NOT EXISTS idx_nexus_memory_nodes_user ON public.nexus_memory_nodes(user_id);
CREATE INDEX IF NOT EXISTS idx_nexus_memory_nodes_type ON public.nexus_memory_nodes(memory_type);
CREATE INDEX IF NOT EXISTS idx_nexus_memory_nodes_embedding ON public.nexus_memory_nodes USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_collective_knowledge_embedding ON public.collective_knowledge USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_nexus_messages_conversation ON public.nexus_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_nexus_conversations_user ON public.nexus_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_nexus_messages_role ON public.nexus_messages(role);

-- ============================================
-- 9. RPC Functions (for vector search)
-- ============================================

-- Search personal memories by vector similarity
CREATE OR REPLACE FUNCTION search_personal_memories(
    query_embedding VECTOR(768),
    target_user_id UUID,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    user_id UUID,
    content TEXT,
    memory_type TEXT,
    tags TEXT[],
    recency_score FLOAT,
    importance_score FLOAT,
    created_at TIMESTAMPTZ,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        mn.id,
        mn.user_id,
        mn.content,
        mn.memory_type,
        mn.tags,
        mn.recency_score,
        mn.importance_score,
        mn.created_at,
        1 - (mn.embedding <=> query_embedding) AS similarity
    FROM public.nexus_memory_nodes mn
    WHERE mn.user_id = target_user_id
      AND mn.is_active = true
      AND mn.embedding IS NOT NULL
    ORDER BY mn.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Search collective knowledge by vector similarity
CREATE OR REPLACE FUNCTION search_collective_knowledge(
    query_embedding VECTOR(768),
    match_count INT DEFAULT 3
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    category TEXT,
    tags TEXT[],
    contributor_count INTEGER,
    quality_score FLOAT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        hm.id,
        hm.content,
        hm.category,
        hm.tags,
        hm.contributor_count,
        hm.quality_score,
        1 - (hm.embedding <=> query_embedding) AS similarity
    FROM public.collective_knowledge hm
    WHERE hm.embedding IS NOT NULL
      AND hm.quality_score >= 0.5
    ORDER BY hm.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ============================================
-- 10. Row Level Security
-- ============================================
ALTER TABLE public.nexus_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nexus_user_identities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nexus_memory_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nexus_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nexus_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.collective_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_evolution ENABLE ROW LEVEL SECURITY;

-- Profiles
CREATE POLICY "Users can view own profile" ON public.nexus_profiles
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.nexus_profiles
    FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Service role full access profiles" ON public.nexus_profiles
    FOR ALL USING (auth.role() = 'service_role');

-- User Identities
CREATE POLICY "Users can view own identity" ON public.nexus_user_identities
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role full access identities" ON public.nexus_user_identities
    FOR ALL USING (auth.role() = 'service_role');

-- Memory Nodes
CREATE POLICY "Users can view own memories" ON public.nexus_memory_nodes
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role full access memories" ON public.nexus_memory_nodes
    FOR ALL USING (auth.role() = 'service_role');

-- Conversations
CREATE POLICY "Users can view own conversations" ON public.nexus_conversations
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own conversations" ON public.nexus_conversations
    FOR DELETE USING (auth.uid() = user_id);
CREATE POLICY "Service role full access conversations" ON public.nexus_conversations
    FOR ALL USING (auth.role() = 'service_role');

-- Messages (via conversation ownership)
CREATE POLICY "Users can view own messages" ON public.nexus_messages
    FOR SELECT USING (
        conversation_id IN (
            SELECT c.id FROM public.nexus_conversations c WHERE c.user_id = auth.uid()
        )
    );
CREATE POLICY "Service role full access messages" ON public.nexus_messages
    FOR ALL USING (auth.role() = 'service_role');

-- Collective Knowledge (readable by all authenticated)
CREATE POLICY "Authenticated can read collective knowledge" ON public.collective_knowledge
    FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Service role full access collective knowledge" ON public.collective_knowledge
    FOR ALL USING (auth.role() = 'service_role');

-- Evolution (readable by all)
CREATE POLICY "Anyone can read evolution" ON public.system_evolution
    FOR SELECT USING (true);
CREATE POLICY "Service role full access evolution" ON public.system_evolution
    FOR ALL USING (auth.role() = 'service_role');
