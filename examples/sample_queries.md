# Sample Queries for Testing

## Hindi (hi-IN) Examples

### Numbers
- Input: `123`
- Expected: `एक सौ बीस तीन`

- Input: `250`
- Expected: `दो सौ पचास`

- Input: `1000`
- Expected: `एक हज़ार`

### Currency
- Input: `₹250`
- Expected: `दो सौ पचास रुपये`

- Input: `₹1000`
- Expected: `एक हज़ार रुपये`

### Dates
- Input: `12/03/2024`
- Expected: `बारह मार्च दो हज़ार चौबीस`

- Input: `01/01/2024`
- Expected: `एक जनवरी दो हज़ार चौबीस`

### Time
- Input: `10:30AM`
- Expected: `सुबह दस बजकर तीस मिनट`

- Input: `2:15PM`
- Expected: `शाम दो बजकर पंद्रह मिनट`

### Units
- Input: `5kg`
- Expected: `पाँच किलोग्राम`

- Input: `10km`
- Expected: `दस किलोमीटर`

### Abbreviations
- Input: `Dr. शर्मा`
- Expected: `डॉक्टर शर्मा`

- Input: `Mr. कुमार`
- Expected: `मिस्टर कुमार`

### Complex Sentences
- Input: `₹250 on 12/03/2024 at 10:30AM`
- Expected: Normalized currency, date, and time

- Input: `Dr. शर्मा ने 5kg चावल ₹500 में खरीदा`
- Expected: Normalized abbreviation, unit, and currency

## Tamil (ta-IN) Examples

### Numbers
- Input: `123`
- Expected: `நூறு இருபது மூன்று`

- Input: `250`
- Expected: `இருநூறு ஐம்பது`

- Input: `1000`
- Expected: `ஆயிரம்`

### Currency
- Input: `₹250`
- Expected: `இருநூறு ஐம்பது ரூபாய்`

- Input: `₹1000`
- Expected: `ஆயிரம் ரூபாய்`

### Dates
- Input: `12/03/2024`
- Expected: `பன்னிரண்டு மார்ச் இரண்டு ஆயிரம் இருபத்து நான்கு`

- Input: `01/01/2024`
- Expected: `ஒன்று ஜனவரி இரண்டு ஆயிரம் இருபத்து நான்கு`

### Time
- Input: `10:30AM`
- Expected: `காலை பத்து மணிக்கு முப்பது நிமிடம்`

- Input: `2:15PM`
- Expected: `மாலை இரண்டு மணிக்கு பதினைந்து நிமிடம்`

### Units
- Input: `5kg`
- Expected: `ஐந்து கிலோகிராம்`

- Input: `10km`
- Expected: `பத்து கிலோமீட்டர்`

### Abbreviations
- Input: `Dr. குமார்`
- Expected: `டாக்டர் குமார்`

- Input: `Mr. ராமன்`
- Expected: `மிஸ்டர் ராமன்`

### Complex Sentences
- Input: `₹250 on 12/03/2024 at 10:30AM`
- Expected: Normalized currency, date, and time

- Input: `Dr. குமார் 5kg அரிசி ₹500க்கு வாங்கினார்`
- Expected: Normalized abbreviation, unit, and currency
