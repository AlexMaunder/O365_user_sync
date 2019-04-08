# O365 usersync & connector setup
LDAP style sync for O365 mailboxes with 3rd party filter. Also sets up required inbound and outbound connectors.



To automate the connector initial setup, integrate the lockdown rules with below Powershell code:


###   params given by python script calling this ps1 script

param(
    [string]$arg1,
    [string]$arg2
)

###   allows ps to be run without needing to be signed - 1 time call that needs to be run to update server settings

###   Set-ExecutionPolicy Unrestricted
###   Set-ExecutionPolicy RemoteSigned

$User = $arg2   ###   'alex@XXXXX.com'   ###   $arg2
$PWord = ConvertTo-SecureString -String $arg1 -AsPlainText -Force   ###   "XXXXX"   ###   $arg1

$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $PWord

###   Exchange Online

# Write-Output $arg1
# Write-Output $User

# $User, $PWord

$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri https://outlook.office365.com/powershell-liveid/ -Credential ${Credential} -Authentication Basic -AllowRedirection
Import-PSSession $Session –AllowClobber

###   inbound mailflow lockdown rule

New-TransportRule "Filter lockdown" -RejectMessageReasonText "Email bypassed MX records" -RejectMessageEnhancedStatusCode "5.7.1" -ExceptIfMessageTypeMatches Calendaring -ExceptIfSenderIpRanges '1.1.1.1/32', '2.2.2.2/20', '3.3.3.3/24' -ExceptIfFromScope InOrganization

###   outbound lockdown rule

New-OutboundConnector "Filter Outbound" -RecipientDomains * -UseMXRecord $false -SmartHosts "outbound.address.com" -TlsSettings EncryptionOnly

###   validate outbound lockdown rule

Validate-OutboundConnector -Identity "Filter Outbound" -Recipients lockdownuser@email.com



###   Get-Mailbox
###   Get-TransportRule
###   New-TransportRule  https://docs.microsoft.com/en-us/powershell/module/exchange/policy-and-compliance/new-transportrule?view=exchange-ps
###   To clear session: Get-PSSession | Remove-PSSession
###   Get-OutboundConnector
###   https://docs.microsoft.com/en-us/powershell/module/exchange/mail-flow/new-outboundconnector?view=exchange-ps
###   Validate-OutboundConnector
###   https://docs.microsoft.com/en-us/powershell/module/exchange/mail-flow/validate-outboundconnector?view=exchange-ps
###   To close sessions: Get-PSSession Remove-PSSession $sessionname

###   Get-PSSession
###   Remove-PSSession -Id 1
