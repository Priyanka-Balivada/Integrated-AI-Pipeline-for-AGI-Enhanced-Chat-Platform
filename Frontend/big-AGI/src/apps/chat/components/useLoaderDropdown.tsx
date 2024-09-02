import * as React from 'react';
import { shallow } from 'zustand/shallow';

import { Box, Button, Checkbox, Divider, FormLabel, IconButton, Input, ListItemButton, ListItemDecorator, Option, Select, Typography } from '@mui/joy';
import BuildCircleIcon from '@mui/icons-material/BuildCircle';
import SettingsIcon from '@mui/icons-material/Settings';

import { DLLM, DLLMId, DModelSourceId, useModelsStore } from '~/modules/llms/store-llms';
import { findVendorById } from '~/modules/llms/vendors/vendors.registry';
import { useIsMobile } from '~/common/components/useMatchMedia';

import { DropdownItems, PageBarDropdownMemo } from '~/common/layout/optima/components/PageBarDropdown';
import { GoodTooltip } from '~/common/components/GoodTooltip';
import { KeyStroke } from '~/common/components/KeyStroke';
import { useOptimaLayout } from '~/common/layout/optima/useOptimaLayout';

import type { SelectSlotsAndSlotProps } from '@mui/joy/Select/SelectProps';

import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import { GoodModal } from '~/common/components/GoodModal';
import { useState } from 'react';
import { ModelsList } from '~/modules/llms/models-modal/ModelsList';
import { DataLoaderOptions } from 'src/data';
import { CloseableMenu } from '~/common/components/CloseableMenu';

function LoaderDropdown() {
  const [showDialog, setShowDialog] = useState(false);

  const toggleModel = () => setShowDialog(!showDialog);

  const isMobile = useIsMobile();
  
  const [loaderForm, setLoaderForm] = useState(
    {
      format: DataLoaderOptions[0],
      url: '',
      prefix: '',
      maxDepth: 0,
      tag: '',
      ignoreID: false,
    }
  )

  const [isHTML, setIsHTML] = useState(false);
  const [isWSR, setIsWSR] = useState(false);

  const handleFormatChange = (event: any) => {
    const value = event.innerText;
    setLoaderForm({ ...loaderForm, format: value as string });
    if(value == 'HTML Tags Reader') {
      setIsHTML(true);
    } else {
      setIsHTML(false);
    }

    if(value == 'Whole Site Reader'){
      setIsWSR(true);
    } else {
      setIsWSR(false);
    }

  }

  const handleSubmit = () => {
    if(isHTML) {
      const form = {
        format: loaderForm.format,
        url: loaderForm.url,
        tag: loaderForm.tag,
        ignoreID: loaderForm.ignoreID,
      }
      
      console.log(form);
    }
    if(isWSR) {
      const form = {
        format: loaderForm.format,
        url: loaderForm.url,
        // tag: loaderForm.tag,
        // ignoreID: loaderForm.ignoreID,
        prefix: loaderForm.prefix,
        maxDepth: loaderForm.maxDepth, 
      }
      
      console.log(form);
    } else {
      const form = {
        format: loaderForm.format,
        url: loaderForm.url,
      }

      console.log(form);
    }
  }

  return (
    <>
      <Select variant="plain" sx={{color: '#b2b5b9', background: '#32383e'}} placeholder='Connectors' value="Connecctor" indicator={<KeyboardArrowDownIcon />}>
        <Box
          sx={{
            overflow: 'auto',
            paddingBlock: 'var(--ListDivider-gap)',
          }}
        >
          <Option value={'loader'} onClick={toggleModel}>
            <Typography className="agi-ellipsize">Connectors</Typography>
          </Option>
        </Box>
      </Select>

      {/* Sources Setup */}
      {showDialog && (
        <GoodModal
          title={
            <>
              Configure <b>Data Loader</b>
            </>
          }
          open
          onClose={toggleModel}
          sx={{ overflow: 'auto' }}
        >
          <Box sx={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
            {!isMobile && <Typography sx={{ mr: 3.5 }}>Format:</Typography>}

            <Select
              variant="outlined"
              value={loaderForm.format}
              onChange={(event) => handleFormatChange(event?.target as any)}
              slotProps={{
                root: { sx: { minWidth: 245 } },
                indicator: { sx: { opacity: 0.5 } },
              }}
            >
              {DataLoaderOptions.map((item) => (
                <Option key={item} value={item}>
                  {item}
                </Option>
              ))}  
            </Select>
          </Box>

          <Box sx={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
            {!isMobile && <Typography sx={{ mr: 1 }}>Base URL:</Typography>}

            <Input
              variant="outlined"
              value={loaderForm.url}
              onChange={(event) => setLoaderForm({ ...loaderForm, url: event.target.value })}
              slotProps={{
                root: { sx: { minWidth: 190 } },
              }}
            />
          </Box>



          {isWSR &&
            <>
            <Box sx={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
              {!isMobile && <Typography sx={{ mr: 4.7 }}>Prefix:</Typography>}

              <Input
                variant="outlined"
                value={loaderForm.prefix}
                onChange={(event) => setLoaderForm({ ...loaderForm, prefix: event.target.value })}
                slotProps={{
                  root: { sx: { minWidth: 190 } },
                }}
              />
            </Box>
            
            <Box sx={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
              {!isMobile && <Typography sx={{ mr: 0 }}>Max Depth:</Typography>}

              <Input
                type='number'
                variant="outlined"
                value={loaderForm.maxDepth}
                onChange={(event) => setLoaderForm({ ...loaderForm, maxDepth: Number(event.target.value) })}
                slotProps={{
                  root: { sx: { minWidth: 190 } },
                }}
              />
            </Box>
          </> 
          }

          {isHTML &&
          <>
            <Box sx={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
              {!isMobile && <Typography sx={{ mr: 6.8 }}>Tag:</Typography>}

              <Input
                variant="outlined"
                value={loaderForm.tag}
                onChange={(event) => setLoaderForm({ ...loaderForm, tag: event.target.value })}
                slotProps={{
                  root: { sx: { minWidth: 190 } },
                }}
              />
            </Box>
            
            <Box sx={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
              {!isMobile && <Typography sx={{ mr: 1 }}>Ignore ID:</Typography>}
              <Checkbox
                name='ignoreID'
                id='ignoreID'
                checked={loaderForm.ignoreID}
                onChange={() => setLoaderForm({ ...loaderForm, ignoreID: !loaderForm.ignoreID })}
              />
            </Box>
          </>
          }

          <Button variant='solid' sx={{ ml: 'auto', minWidth: 100 }} onClick={handleSubmit}>Submit</Button>

          <Divider />
        </GoodModal>
      )}
    </>
  );
}

export function useLoaderDropdown() {
  const chatLoaderDropdown = React.useMemo(() => <LoaderDropdown />, []);

  return { chatLoaderDropdown };
}
