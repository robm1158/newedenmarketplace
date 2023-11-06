import 'react-pro-sidebar/dist/css/styles.css';
import React from 'react';
import { ProSidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';
import marketGroupsJSON from '../../constants/marketGroups.json';
import { ItemEnum } from '../../constants/ItemEnum';
import './Sidebar.css';

const CustomSidebar = ({ handleSidebarClick }) => {

    const REVERSED_ITEM_ENUM = Object.keys(ItemEnum).reduce((obj, key) => {
        obj[ItemEnum[key]] = key;
        return obj;
    }, {});

    // Helper function to check if the word is a Roman numeral
    const isRomanNumeral = (word) => {
        // Regex to match a Roman numeral
        const romanRegex = /^(?=[MDCLXVI])(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))$/i;
        return romanRegex.test(word);
    };

    // Function to capitalize each segment of the itemName properly, including Roman numerals
    const formatItemName = (itemName) => {
        if (!itemName) return '';

        // Split the itemName into words, then map through each word
        return itemName.toLowerCase().split('_').map(word => {
            // If the word is a Roman numeral, capitalize all letters, otherwise just capitalize the first letter
            return isRomanNumeral(word) ? word.toUpperCase() : word.charAt(0).toUpperCase() + word.slice(1);
        }).join(' ');
    };

    const renderTypes = (types, depth = 0) => {
        return types.map(typeId => {
          const itemName = REVERSED_ITEM_ENUM[typeId];
          const formattedItemName = itemName ? formatItemName(itemName) : '';
          // Define the class name based on depth
          let itemClassName = 'menuItem';
          if (depth === 1) {
            itemClassName = 'submenuItem';
          } else if (depth > 1) {
            itemClassName = 'deepSubmenuItem';
          }
      
          return (
            <MenuItem
              key={typeId}
              className={itemClassName} // Use className as a string
              data-tooltip={formattedItemName} // Tooltip text
              onClick={(event) => {
                event.stopPropagation(); // Stop the event from bubbling up
                handleSidebarClick(typeId, 'type');
              }}
            >
              {formattedItemName}
            </MenuItem>
          );
        });
      };
      

    const renderSidebarItem = (group, depth = 0) => {
        return (
          <SubMenu
            key={group.market_group_id}
            title={group.name}
            
            // Use the icon class here as a string if needed
            icon={<img src={group.iconFile} alt={group.name} className="icon" />} 
            onClick={(event) => {
              event.stopPropagation(); // Stop the event from bubbling up
              handleSidebarClick(group.market_group_id, 'group');
            }}
          >
            {renderTypes(group.types, depth + 1)}
            {group.children.map(childGroup => renderSidebarItem(childGroup, depth + 1))}
          </SubMenu>
        );
    };

    return (
        <ProSidebar>
            <Menu>
                {marketGroupsJSON.map(renderSidebarItem)}
            </Menu>
        </ProSidebar>
    );
};

export default CustomSidebar;
