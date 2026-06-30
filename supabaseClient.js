import { createClient } from '@supabase/supabase-js'

// You can find these two keys in your Supabase Dashboard under Settings -> API
const SUPABASE_URL = 'https://khnwfpcuvcyxztgoyhpr.supabase.co'
const SUPABASE_ANON_KEY = 'sb_publishable_gZOCkHy6H8C03dRVRXJO7w_en4rfq9J'

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

import { supabase } from './supabaseClient'

import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'YOUR_SUPABASE_PROJECT_URL'
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_PUBLIC_KEY'

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)