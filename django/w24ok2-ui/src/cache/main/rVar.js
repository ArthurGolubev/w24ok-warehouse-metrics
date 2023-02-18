import { makeVar } from "@apollo/client";

export const TLSOptions = makeVar({
    // era: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long',
    // timezone: 'UTC',
    // hour: 'numeric',
    // minute: 'numeric',
    // second: 'numeric'
})

export const selectedMonthToMonthSubject = makeVar({title: 'выручки', key: 'paid', yaxis: 'Выручка'})
export const selectedUsersPlot = makeVar('absolute')
export const topQuantity = makeVar({users: 30, orgs: 30})
export const selectTopRange = makeVar('month')