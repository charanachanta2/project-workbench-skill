import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Live, Totals } from '../types'

const PANE = 'token-meter'
const zeroTotals: Totals = { turns: 0, input: 0, output: 0, cacheRead: 0, cacheWrite: 0, lastModel: '' }
const zeroLive: Live = { tokens: 0, window: 0, percent: 0, usd: 0, limits: [] }

// Change the shape tag when the stored fields change.
const totals = atom({ plugin: 'token-meter', key: 'totals' } as const, zeroTotals, { shape: 'totals-1' })
const live = atom({ plugin: 'token-meter', key: 'live' } as const, zeroLive, { shape: 'live-1' })

const fmt = (n: number) => n.toLocaleString('en-US')

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'token-meter', description: 'Open the live token meter pane' })
    void $.ui.open({ id: PANE, title: 'Token meter' })
    return next(e)
  })

  on('command.run', { command: 'token-meter' }, async $ => {
    await $.ui.open({ id: PANE, title: 'Token meter' })
    return { text: 'Token meter opened.' }
  })

  // Per-turn tokens as the API counted them, summed for the session.
  on('turn.complete', async ($, e, next) => {
    const ran = await next(e)
    const u = ran.usage
    if (u) {
      await update($, totals, t => ({
        turns: t.turns + 1,
        input: t.input + u.input_tokens,
        output: t.output + u.output_tokens,
        cacheRead: t.cacheRead + u.cache_read_input_tokens,
        cacheWrite: t.cacheWrite + u.cache_creation_input_tokens,
        lastModel: u.model,
      }))
    }
    return ran
  })

  // Context fill, cost and rate limits, pushed after each turn.
  on('session.measure', async ($, e, next) => {
    await update($, live, () => ({
      tokens: e.context.tokens ?? 0,
      window: e.context.window,
      percent: e.context.percent ?? 0,
      usd: e.cost?.usd ?? 0,
      limits: e.rateLimits.map(r => ({ kind: r.kind, percentUsed: r.percentUsed })),
    }))
    return next(e)
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const t = await read($, totals)
    const l = await read($, live)
    const bar = (p: number) => {
      const n = Math.round(Math.min(100, Math.max(0, p)) / 5)
      return '[' + '#'.repeat(n) + '-'.repeat(20 - n) + '] ' + p + '%'
    }

    return (
      <Box flexDirection="column">
        <Text bold>Context window</Text>
        <Text>{bar(l.percent)}</Text>
        <Text dimColor>{fmt(l.tokens)} / {fmt(l.window)} tokens</Text>
        <Text bold>Session totals ({t.turns} turns)</Text>
        <Text>input (uncached): {fmt(t.input)}</Text>
        <Text>output: {fmt(t.output)}</Text>
        <Text>cache read: {fmt(t.cacheRead)}</Text>
        <Text>cache write: {fmt(t.cacheWrite)}</Text>
        <Text bold>Cost</Text>
        <Text>${l.usd.toFixed(4)}</Text>
        {l.limits.map(r => (
          <Text>{r.kind}: {bar(r.percentUsed)}</Text>
        ))}
        {t.lastModel !== '' && <Text dimColor>model: {t.lastModel}</Text>}
      </Box>
    )
  })
}
