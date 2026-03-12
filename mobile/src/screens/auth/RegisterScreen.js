import React from 'react';

import ScreenContainer from '../../components/ScreenContainer';

export default function RegisterScreen() {
  return (
    <ScreenContainer
      title="Créer un compte"
      description="L'inscription sera connectée au backend Django via JWT."
    />
  );
}
