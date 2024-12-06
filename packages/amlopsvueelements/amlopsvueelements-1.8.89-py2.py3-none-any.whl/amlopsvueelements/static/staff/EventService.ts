import moment from 'moment'
import type { EventInput } from '@fullcalendar/core'
import { RRule, type Options, datetime } from 'rrule'
import type { Resource } from '@/models/Resource'
import type { BlanketEntry, PersonWithEntries, SpecificEntry } from '@/models/Entry'
import entryService from '@/services/EntryService'
import { isAllDay } from '@/utils/date'

type RRuleOptions = Partial<Options>

const constructEvent = (
  person: PersonWithEntries,
  entry: BlanketEntry | SpecificEntry,
  isSpecificEntry: boolean = false
): EventInput => {
  const teamName = person.teams.find((team) => team.aml_team_id === entry.team)?.team
    ? true
    : isAllDay([
        `${entry.start_date} ${entry.start_hour}`,
        `${entry.end_date ? entry.end_date : entry.start_date} ${entry.end_hour}`
      ])

  const event = {
    id: `${isSpecificEntry ? 'specific' : 'blanket'}-${entry.id}-${entry.team}`,
    resourceId: `${person.id}-${entry.team}`,
    title: entry.entry_type.name,
    backgroundColor: entry.entry_type.background,
    rrule: isSpecificEntry
      ? {
          freq: RRule.DAILY,
          bymonthday: (entry as SpecificEntry).applied_on_dates,
          dtstart: `${entry.start_date}T${
            entry.entry_type.requires_full_workday ? '00:00:00' : entry.start_hour
          }Z`,
          ...(entry.end_date
            ? { until: moment.utc(entry.end_date).add(1, 'day').format('YYYY-MM-DD') }
            : {})
        }
      : {
          freq: RRule.WEEKLY,
          ...((entry as BlanketEntry).applied_on_weeks
            ? {
                byweekno:
                  (entry as BlanketEntry).applied_on_weeks[0] === 0
                    ? []
                    : (entry as BlanketEntry).applied_on_weeks.map((wn) =>
                        moment(entry.start_date)
                          .add(wn - 1, 'weeks')
                          .get('week')
                      )
              }
            : {}),
          byweekday: (entry as BlanketEntry).applied_on_days.map((wd) => wd - 1),
          dtstart: `${entry.start_date}T${
            entry.entry_type.requires_full_workday ? '00:00:00' : entry.start_hour
          }Z`,
          ...(entry.end_date
            ? {
                until: moment
                  .utc(entry.end_date)
                  .add(entry.start_hour, 'h')
                  .format('YYYY-MM-DD HH:mm')
              }
            : {})
        },
    exdate: !isSpecificEntry
      ? ('excluded_dates' in entry ? entry.excluded_dates : []).map(
          (excluded_date) =>
            moment(excluded_date).format('YYYY-MM-DD') + 'T' + entry.start_hour + 'Z'
        )
      : [],
    duration: entry.entry_type.requires_full_workday
      ? moment.duration(1, 'day').asMilliseconds()
      : moment.duration(entry.end_hour).subtract(entry.start_hour).asMilliseconds(),
    extendedProps: {
      ...entry,
      person: {
        id: 0,
        name: `${person.name} - ${teamName}`,
        aml_team_id: entry.team,
        person_id: person.id,
        timezone: person.timezone
      }
    }
  }
  if (event.duration < 0) {
    event.duration += 24 * 3600 * 1000
  }
  return event
}

const fetchEvents = async (
  start: Date,
  end: Date,
  teams: string[]
): Promise<{ events: EventInput[]; resources: Resource[] }> => {
  const start_date = moment(start).subtract(1, 'day').format('YYYY-MM-DD')
  const end_date = moment(end).add(1, 'day').format('YYYY-MM-DD')
  const peopleWithEntries = await entryService.getValidEntries({ start_date, end_date, teams })

  const events: EventInput[] = [],
    resources: Resource[] = []

  if (!peopleWithEntries || !peopleWithEntries.length) {
    return {
      events,
      resources
    }
  }

  for (const personWithEntries of peopleWithEntries) {
    for (const team of personWithEntries.teams) {
      resources.push({
        id: `${personWithEntries.id}-${team.aml_team_id}`,
        title: personWithEntries.name,
        groupId: team.team,
        extendedProps: {
          person: {
            id: team.id,
            name: `${personWithEntries.name} - ${team.team}`,
            aml_team_id: team.aml_team_id,
            timezone: personWithEntries.timezone,
            person_id: personWithEntries.id
          },
          team: team.team,
          role: team.role
        }
      })
    }

    const specificEvents = [],
      blanketEvents = []
    for (const specificEntry of personWithEntries.specific_entries) {
      specificEvents.push(constructEvent(personWithEntries, specificEntry, true))
    }

    for (const blanketEntry of personWithEntries.blanket_entries) {
      const event = constructEvent(personWithEntries, blanketEntry)

      const startSelf = moment((event.rrule as RRuleOptions)?.dtstart)
      const endSelf = moment((event.rrule as RRuleOptions)?.until)
      const overrideSpecificEvent = specificEvents.find((specificEvent) => {
        if (
          specificEvent.extendedProps?.person.aml_team_id != event.extendedProps?.person.aml_team_id
        )
          return false
        const startSpecific = moment((specificEvent.rrule as RRuleOptions)?.dtstart)
        const endSpecific = moment((specificEvent.rrule as RRuleOptions)?.until)
        return (
          startSpecific.isBetween(startSelf, endSelf) ||
          endSpecific.isBetween(startSelf, endSelf) ||
          (startSpecific.isSameOrBefore(startSelf) && endSpecific.isSameOrAfter(endSelf))
        )
      })
      if (overrideSpecificEvent) {
        event.exrule = {}
        Object.assign(event.exrule, overrideSpecificEvent.rrule)
        event.exrule.dtstart = (event.rrule as RRuleOptions)?.dtstart
      }

      blanketEvents.push(event)
    }

    events.push(...blanketEvents)
    events.push(...specificEvents)
  }

  return { events, resources }
}

export default {
  fetchEvents
}
