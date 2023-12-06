import nfc

# Create a ContactlessFrontend instance
clf = nfc.ContactlessFrontend('usb')

# Use the sense() method to search for a proximity target
target = clf.sense(nfc.clf.RemoteTarget('106A'), nfc.clf.RemoteTarget('106B'), nfc.clf.RemoteTarget('212F'))

# Print the target
print(target)

# Use the activate() function to activate the target and return a Type3Tag instance
tag = nfc.tag.activate(clf, target)

# Print the tag
print(tag)
