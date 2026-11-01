export type Totals = {
  turns: number
  input: number
  output: number
  cacheRead: number
  cacheWrite: number
  lastModel: string
}
export type Live = {
  tokens: number
  window: number
  percent: number
  usd: number
  limits: { kind: string; percentUsed: number }[]
}

declare module 'claude-code' {
  interface PluginState {
    'token-meter': { totals: Shaped<Totals>; live: Shaped<Live> }
  }
}
