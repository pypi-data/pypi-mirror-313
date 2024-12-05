hardware_fragment = """
fragment HardwareFragment on Hardware {
  id
  pk
  name
  slug
  createdAt
  updatedAt
  isAvailable
  isOnline
  isQuarantined
  isHealthy
  hostname
  sshUsername
  capabilities {
    id
    pk
  }
  activeReservation {
    id
    pk
  }
}
"""
